from decimal import Decimal
from django.db import transaction
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import (Profile, UploadedDocument, AgentAssignment, VerificationVisit,
    LocationConsent, LocationRecord, Contract, CollectionVisit, Notification,
    FraudAlert, SystemSetting, Loan, LoanApplication, Payment, AuditLog)


def profile_for(user):
    return get_object_or_404(Profile, user=user)


def staff(p):
    return p.role in ('ADMIN','ANALYST')

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = ['id','document_type','file','status','rejection_reason','created_at','verified_at']
        read_only_fields = ['id','status','rejection_reason','created_at','verified_at']

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        return UploadedDocument.objects.all() if staff(p) else UploadedDocument.objects.filter(profile=p)
    def perform_create(self, serializer): serializer.save(profile=profile_for(self.request.user))
    @action(detail=True, methods=['post'], url_path='verify')
    def verify(self, request, pk=None):
        p=profile_for(request.user)
        if not staff(p): return Response({'detail':'Accès refusé.'}, status=403)
        doc=self.get_object(); ok=bool(request.data.get('approved', True))
        doc.status='VERIFIED' if ok else 'REJECTED'; doc.rejection_reason='' if ok else str(request.data.get('reason','Document non conforme.'))
        doc.verified_by=p; doc.verified_at=timezone.now(); doc.save(update_fields=['status','rejection_reason','verified_by','verified_at'])
        AuditLog.objects.create(actor=p,action='DOCUMENT_VERIFIED' if ok else 'DOCUMENT_REJECTED',object_type='UploadedDocument',object_id=str(doc.id))
        return Response(DocumentSerializer(doc).data)

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=AgentAssignment
        fields='__all__'
        read_only_fields=['assigned_by','created_at']

class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class=AssignmentSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        if p.role=='AGENT': return AgentAssignment.objects.filter(agent=p)
        if staff(p): return AgentAssignment.objects.all()
        return AgentAssignment.objects.filter(application__profile=p)
    def perform_create(self, serializer):
        p=profile_for(self.request.user)
        if not staff(p): raise serializers.ValidationError('Seul le personnel habilité peut assigner un agent.')
        agent_id=self.request.data.get('agent')
        agent=get_object_or_404(Profile,id=agent_id,role='AGENT')
        serializer.save(assigned_by=p,agent=agent)

class VerificationVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model=VerificationVisit
        fields='__all__'

class VerificationVisitViewSet(viewsets.ModelViewSet):
    serializer_class=VerificationVisitSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        return VerificationVisit.objects.all() if staff(p) else VerificationVisit.objects.filter(agent=p)
    def perform_create(self, serializer):
        p=profile_for(self.request.user)
        if p.role!='AGENT' and not staff(p): raise serializers.ValidationError('Agent requis.')
        agent=get_object_or_404(Profile,id=self.request.data.get('agent',p.id),role='AGENT')
        serializer.save(agent=agent)
    @action(detail=True,methods=['post'],url_path='complete')
    def complete(self,request,pk=None):
        visit=self.get_object(); p=profile_for(request.user)
        if p.role=='AGENT' and visit.agent_id!=p.id: return Response({'detail':'Accès refusé.'},status=403)
        visit.result=request.data.get('result','REVIEW'); visit.notes=request.data.get('notes',''); visit.visited_at=timezone.now()
        if request.data.get('latitude') is not None: visit.latitude=request.data['latitude']
        if request.data.get('longitude') is not None: visit.longitude=request.data['longitude']
        visit.save(); return Response(VerificationVisitSerializer(visit).data)

class LocationConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model=LocationConsent
        fields=['id','purpose','granted','version','granted_at']
        read_only_fields=['id','granted_at']

class LocationConsentViewSet(viewsets.ModelViewSet):
    serializer_class=LocationConsentSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self): return LocationConsent.objects.filter(profile=profile_for(self.request.user))
    def perform_create(self,serializer):
        granted=bool(self.request.data.get('granted',False))
        serializer.save(profile=profile_for(self.request.user),granted=granted,granted_at=timezone.now() if granted else None)

class LocationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=LocationRecord
        fields='__all__'
        read_only_fields=['profile','created_at']

class LocationRecordViewSet(viewsets.ModelViewSet):
    serializer_class=LocationRecordSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        if staff(p): return LocationRecord.objects.all()
        return LocationRecord.objects.filter(profile=p)
    def perform_create(self,serializer):
        p=profile_for(self.request.user); consent_id=self.request.data.get('consent')
        consent=get_object_or_404(LocationConsent,id=consent_id,profile=p,granted=True)
        serializer.save(profile=p,consent=consent)

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contract
        fields='__all__'
        read_only_fields=['created_at','signed_at']

class ContractViewSet(viewsets.ModelViewSet):
    serializer_class=ContractSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        return Contract.objects.all() if staff(p) else Contract.objects.filter(loan__profile=p)
    @action(detail=True,methods=['post'],url_path='sign')
    def sign(self,request,pk=None):
        contract=self.get_object(); p=profile_for(request.user)
        if contract.loan.profile_id!=p.id and not staff(p): return Response({'detail':'Accès refusé.'},status=403)
        if contract.status not in ('DRAFT','PENDING'): return Response({'detail':'Contrat non signable.'},status=400)
        contract.status='SIGNED'; contract.signed_at=timezone.now(); contract.save(update_fields=['status','signed_at'])
        AuditLog.objects.create(actor=p,action='CONTRACT_SIGNED',object_type='Contract',object_id=str(contract.id))
        return Response(ContractSerializer(contract).data)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=CollectionVisit
        fields='__all__'
        read_only_fields=['agent']

class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class=CollectionSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        if p.role=='AGENT': return CollectionVisit.objects.filter(agent=p)
        if staff(p): return CollectionVisit.objects.all()
        return CollectionVisit.objects.filter(loan__profile=p)
    def perform_create(self,serializer):
        p=profile_for(self.request.user)
        if p.role!='AGENT' and not staff(p): raise serializers.ValidationError('Agent requis.')
        serializer.save(agent=p if p.role=='AGENT' else get_object_or_404(Profile,id=self.request.data.get('agent'),role='AGENT'))
    @action(detail=True,methods=['post'],url_path='complete')
    def complete(self,request,pk=None):
        visit=self.get_object(); p=profile_for(request.user)
        if p.role=='AGENT' and visit.agent_id!=p.id: return Response({'detail':'Accès refusé.'},status=403)
        visit.result=request.data.get('result',visit.result); visit.notes=request.data.get('notes',visit.notes); visit.visited_at=timezone.now()
        visit.save(); return Response(CollectionSerializer(visit).data)

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields='__all__'
        read_only_fields=['profile','created_at']

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class=NotificationSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        return Notification.objects.all() if staff(p) else Notification.objects.filter(profile=p)
    def perform_create(self,serializer):
        p=profile_for(self.request.user)
        if not staff(p): raise serializers.ValidationError('Personnel habilité requis.')
        serializer.save()
    @action(detail=True,methods=['post'],url_path='read')
    def read(self,request,pk=None):
        n=self.get_object(); n.read_at=timezone.now(); n.save(update_fields=['read_at']); return Response(NotificationSerializer(n).data)

class FraudSerializer(serializers.ModelSerializer):
    class Meta:
        model=FraudAlert
        fields='__all__'
        read_only_fields=['created_at','resolved_at']

class FraudViewSet(viewsets.ModelViewSet):
    serializer_class=FraudSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        return FraudAlert.objects.all() if staff(p) else FraudAlert.objects.filter(profile=p)
    @action(detail=True,methods=['post'],url_path='resolve')
    def resolve(self,request,pk=None):
        p=profile_for(request.user)
        if not staff(p): return Response({'detail':'Accès refusé.'},status=403)
        alert=self.get_object(); alert.status=request.data.get('status','RESOLVED'); alert.resolved_at=timezone.now(); alert.save(update_fields=['status','resolved_at'])
        return Response(FraudSerializer(alert).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    p=profile_for(request.user)
    loans=Loan.objects.all() if staff(p) else Loan.objects.filter(profile=p)
    applications=LoanApplication.objects.all() if staff(p) else LoanApplication.objects.filter(profile=p)
    payments=Payment.objects.all() if staff(p) else Payment.objects.filter(loan__profile=p)
    data={'applications':applications.count(),'active_loans':loans.filter(status='ACTIVE').count(),'late_loans':loans.filter(status='LATE').count(),'paid_loans':loans.filter(status='PAID').count(),'total_principal':loans.aggregate(v=Sum('principal'))['v'] or Decimal('0'),'total_collected':payments.aggregate(v=Sum('amount'))['v'] or Decimal('0')}
    if staff(p): data['open_fraud_alerts']=FraudAlert.objects.filter(status='OPEN').count(); data['pending_documents']=UploadedDocument.objects.filter(status='PENDING').count(); data['agents']=Profile.objects.filter(role='AGENT').count()
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def qr_lookup(request, token):
    p=profile_for(request.user)
    if p.role not in ('AGENT','ADMIN','ANALYST'): return Response({'detail':'Agent ou administrateur requis.'},status=403)
    loan=get_object_or_404(Loan,qr_token=token)
    remaining=loan.total_due-(loan.payments.aggregate(v=Sum('amount'))['v'] or Decimal('0'))
    return Response({'loan_id':loan.id,'client_id':loan.profile_id,'status':loan.status,'principal':loan.principal,'total_due':loan.total_due,'total_paid':loan.total_due-remaining,'remaining':max(Decimal('0'),remaining),'installments':list(loan.installments.values('number','due_date','amount_due','amount_paid','status'))})
