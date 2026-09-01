from decimal import Decimal
from datetime import timedelta
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import (Profile, Address, Employment, Business, Reference, LoanApplication,
    Loan, Installment, Payment, PaymentReceipt, AuditLog, UploadedDocument, Contract,
    Notification, FraudAlert)
from .serializers import ProfileSerializer, AddressSerializer, EmploymentSerializer, BusinessSerializer, ReferenceSerializer, ApplicationSerializer, LoanSerializer, PaymentSerializer


def profile_for(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def score_application(app):
    p = app.profile
    score = 0
    if p.verified and p.national_id: score += 15
    employment = getattr(p, 'employment', None)
    businesses = p.businesses.filter(verified=True)
    if employment and employment.verified and employment.monthly_income > 0: score += 20
    elif businesses.exists(): score += 15
    if employment and employment.years_active >= 1: score += 10
    if businesses.filter(years_active__gte=1).exists(): score += 10
    disposable = max(Decimal('0'), app.monthly_income - app.monthly_expenses)
    if disposable > 0: score += 20
    if app.amount <= max(Decimal('1'), disposable * 2): score += 15
    if p.references.filter(verified=True).count() >= 2: score += 10
    if p.documents.filter(document_type='NATIONAL_ID', status='VERIFIED').exists(): score += 5
    score = min(score, 100)
    risk = 'A' if score >= 80 else 'B' if score >= 65 else 'C' if score >= 50 else 'D'
    return score, risk


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return Profile.objects.filter(user=self.request.user)
    def perform_create(self, serializer): serializer.save(user=self.request.user)

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return Address.objects.filter(profile=profile_for(self.request.user))
    def perform_create(self, serializer): serializer.save(profile=profile_for(self.request.user))

class EmploymentViewSet(viewsets.ModelViewSet):
    serializer_class = EmploymentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return Employment.objects.filter(profile=profile_for(self.request.user))
    def perform_create(self, serializer): serializer.save(profile=profile_for(self.request.user))

class BusinessViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return Business.objects.filter(profile=profile_for(self.request.user))
    def perform_create(self, serializer): serializer.save(profile=profile_for(self.request.user))

class ReferenceViewSet(viewsets.ModelViewSet):
    serializer_class = ReferenceSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return Reference.objects.filter(profile=profile_for(self.request.user))
    def perform_create(self, serializer): serializer.save(profile=profile_for(self.request.user))

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        p = profile_for(self.request.user)
        return LoanApplication.objects.all() if p.role in ('ADMIN','ANALYST') else LoanApplication.objects.filter(profile=p)
    def perform_create(self, serializer): serializer.save(profile=profile_for(self.request.user))

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        app = self.get_object(); p = profile_for(request.user)
        if app.status not in ('DRAFT','MORE_INFO'):
            return Response({'detail':'Cette demande ne peut plus être soumise.'}, status=400)
        missing=[]
        if not p.national_id: missing.append('pièce d’identité')
        if not p.documents.filter(document_type='NATIONAL_ID').exists(): missing.append('document d’identité')
        if not (app.monthly_income > 0 or p.businesses.exists()): missing.append('source de revenus ou commerce')
        if p.references.count() < 2: missing.append('au moins deux références')
        if missing:
            app.status='MORE_INFO'; app.save(update_fields=['status','updated_at'])
            return Response({'detail':'Dossier incomplet.','missing':missing,'application':ApplicationSerializer(app).data},status=400)
        score, risk = score_application(app)
        app.score, app.risk_class, app.status, app.submitted_at = score, risk, 'VERIFYING', timezone.now()
        app.save(update_fields=['score','risk_class','status','submitted_at','updated_at'])
        if score < 50:
            FraudAlert.objects.create(profile=p,application=app,rule='LOW_CREDIT_SCORE',severity='MEDIUM',details={'score':score,'risk':risk})
        AuditLog.objects.create(actor=p, action='APPLICATION_SUBMITTED', object_type='LoanApplication', object_id=str(app.id), metadata={'score':score,'risk':risk})
        return Response(ApplicationSerializer(app).data)

    @action(detail=True, methods=['post'], url_path='decision')
    def decision(self, request, pk=None):
        p = profile_for(request.user)
        if p.role not in ('ADMIN','ANALYST'): return Response({'detail':'Accès refusé.'}, status=403)
        app = self.get_object(); decision = request.data.get('decision')
        if decision not in ('APPROVED','REJECTED','MORE_INFO'): return Response({'detail':'Décision invalide.'}, status=400)
        if decision == 'APPROVED' and app.score < 50:
            return Response({'detail':'Une demande avec un score inférieur à 50 nécessite une décision manuelle renforcée.'},status=400)
        app.status = decision; app.save(update_fields=['status','updated_at'])
        AuditLog.objects.create(actor=p, action=f'APPLICATION_{decision}', object_type='LoanApplication', object_id=str(app.id))
        if decision == 'APPROVED':
            if hasattr(app, 'loan'): return Response(LoanSerializer(app.loan).data)
            total = Decimal(request.data.get('total_due', app.amount))
            if total < app.amount: return Response({'detail':'Le total dû ne peut pas être inférieur au capital.'},status=400)
            with transaction.atomic():
                loan = Loan.objects.create(application=app, profile=app.profile, principal=app.amount, total_due=total)
                count = max(1, app.duration_days // (7 if app.frequency == 'WEEKLY' else 1))
                if app.frequency == 'MONTHLY': count = max(1, app.duration_days // 30)
                installment_amount = (total / count).quantize(Decimal('0.01'))
                start = timezone.localdate() + timedelta(days=7 if app.frequency == 'WEEKLY' else 30)
                remainder = total - installment_amount * count
                for n in range(1, count + 1):
                    amount = installment_amount + (remainder if n == count else Decimal('0'))
                    due = start + timedelta(days=(n-1) * (30 if app.frequency == 'MONTHLY' else 7))
                    Installment.objects.create(loan=loan, number=n, due_date=due, amount_due=amount)
                Contract.objects.create(loan=loan,status='PENDING',terms={'principal':str(app.amount),'total_due':str(total),'duration_days':app.duration_days,'frequency':app.frequency,'purpose':app.purpose})
                Notification.objects.create(profile=app.profile,title='Demande approuvée',message='Votre demande DEFA a été approuvée. Consultez votre proposition et votre contrat.',kind='LOAN_APPROVED')
            return Response(LoanSerializer(loan).data, status=201)
        Notification.objects.create(profile=app.profile,title='Mise à jour de votre demande',message='Votre dossier DEFA a été mis à jour. Consultez votre espace client pour les détails.',kind=f'APPLICATION_{decision}')
        return Response(ApplicationSerializer(app).data)

class LoanViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        return Loan.objects.all() if p.role in ('ADMIN','ANALYST','AGENT') else Loan.objects.filter(profile=p)
    @action(detail=True, methods=['get'], url_path='by-qr')
    def by_qr(self, request, pk=None): return Response(LoanSerializer(self.get_object()).data)

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        return Payment.objects.all() if p.role in ('ADMIN','AGENT','ANALYST') else Payment.objects.filter(loan__profile=p)
    def create(self, request, *args, **kwargs):
        p=profile_for(request.user)
        if p.role not in ('ADMIN','AGENT'):
            return Response({'detail':'Seuls les agents autorisés peuvent enregistrer un encaissement.'}, status=403)
        serializer=self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            loan=Loan.objects.select_for_update().get(pk=serializer.validated_data['loan'].pk)
            paid=loan.payments.aggregate(v=Sum('amount'))['v'] or Decimal('0')
            remaining_loan=loan.total_due-paid
            if serializer.validated_data['amount'] > remaining_loan:
                return Response({'detail':'Le montant dépasse le solde du prêt.','remaining':str(remaining_loan)},status=400)
            payment=serializer.save(agent=p)
            remaining = payment.amount
            for inst in loan.installments.select_for_update().order_by('number'):
                room=max(Decimal('0'), inst.amount_due-inst.amount_paid)
                applied=min(room, remaining)
                if applied:
                    inst.amount_paid += applied
                    inst.status='PAID' if inst.amount_paid >= inst.amount_due else 'PARTIAL'
                    inst.save(update_fields=['amount_paid','status'])
                    remaining -= applied
                if remaining <= 0: break
            receipt=PaymentReceipt.objects.create(payment=payment, number=f'DEFA-{timezone.now():%Y%m%d}-{str(payment.id)[:8].upper()}')
            total_paid=loan.payments.aggregate(total=Sum('amount'))['total'] or Decimal('0')
            if total_paid >= loan.total_due:
                loan.status='PAID'; loan.save(update_fields=['status'])
            AuditLog.objects.create(actor=p, action='PAYMENT_RECORDED', object_type='Payment', object_id=str(payment.id), metadata={'amount':str(payment.amount),'receipt':receipt.number})
            Notification.objects.create(profile=loan.profile,title='Paiement enregistré',message=f'Votre paiement de {payment.amount} a été enregistré. Reçu {receipt.number}.',kind='PAYMENT')
        return Response({'payment':PaymentSerializer(payment).data,'receipt':{'number':receipt.number}}, status=201)

@api_view(['GET'])
@permission_classes([AllowAny])
def health(request): return Response({'service':'DEFA API','status':'ok'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    p=profile_for(request.user)
    return Response({'id':p.id,'user':request.user.username,'role':p.role,'verified':p.verified,'phone':p.phone})