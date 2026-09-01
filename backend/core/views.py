from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile, Address, Employment, Business, Reference, LoanApplication, Loan, Installment, Payment, PaymentReceipt, Consent, AuditLog
from .serializers import ProfileSerializer, AddressSerializer, EmploymentSerializer, BusinessSerializer, ReferenceSerializer, ApplicationSerializer, LoanSerializer, InstallmentSerializer, PaymentSerializer, ReceiptSerializer


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
        app = self.get_object()
        if app.status not in ('DRAFT','MORE_INFO'): return Response({'detail':'Cette demande ne peut plus être soumise.'}, status=400)
        score, risk = score_application(app)
        app.score, app.risk_class, app.status, app.submitted_at = score, risk, 'VERIFYING', timezone.now()
        app.save(update_fields=['score','risk_class','status','submitted_at','updated_at'])
        AuditLog.objects.create(actor=profile_for(request.user), action='APPLICATION_SUBMITTED', object_type='LoanApplication', object_id=str(app.id), metadata={'score':score,'risk':risk})
        return Response(ApplicationSerializer(app).data)
    @action(detail=True, methods=['post'], url_path='decision')
    def decision(self, request, pk=None):
        p = profile_for(request.user)
        if p.role not in ('ADMIN','ANALYST'): return Response({'detail':'Accès refusé.'}, status=403)
        app = self.get_object(); decision = request.data.get('decision')
        if decision not in ('APPROVED','REJECTED','MORE_INFO'): return Response({'detail':'Décision invalide.'}, status=400)
        app.status = decision; app.save(update_fields=['status','updated_at'])
        AuditLog.objects.create(actor=p, action=f'APPLICATION_{decision}', object_type='LoanApplication', object_id=str(app.id))
        if decision == 'APPROVED':
            total = Decimal(request.data.get('total_due', app.amount))
            loan = Loan.objects.create(application=app, profile=app.profile, principal=app.amount, total_due=total)
            return Response(LoanSerializer(loan).data, status=201)
        return Response(ApplicationSerializer(app).data)

class LoanViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        return Loan.objects.all() if p.role in ('ADMIN','ANALYST','AGENT') else Loan.objects.filter(profile=p)
    @action(detail=True, methods=['get'], url_path='by-qr')
    def by_qr(self, request, pk=None):
        return Response(LoanSerializer(self.get_object()).data)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        p=profile_for(self.request.user)
        return Payment.objects.all() if p.role in ('ADMIN','AGENT','ANALYST') else Payment.objects.filter(loan__profile=p)
    @transaction.atomic
    def perform_create(self, serializer):
        p=profile_for(self.request.user)
        if p.role not in ('ADMIN','AGENT'): raise PermissionError('Agent requis')
        payment=serializer.save(agent=p)
        remaining = payment.amount
        for inst in payment.loan.installments.select_for_update().order_by('number'):
            room=max(Decimal('0'), inst.amount_due-inst.amount_paid)
            applied=min(room, remaining)
            if applied:
                inst.amount_paid += applied
                inst.status='PAID' if inst.amount_paid >= inst.amount_due else 'PARTIAL'
                inst.save(update_fields=['amount_paid','status'])
                remaining -= applied
            if remaining <= 0: break
        receipt=PaymentReceipt.objects.create(payment=payment, number=f'DEFA-{timezone.now():%Y%m%d}-{str(payment.id)[:8].upper()}')
        total_paid=payment.loan.payments.aggregate(total=__import__('django.db.models',fromlist=['Sum']).Sum('amount'))['total'] or 0
        if total_paid >= payment.loan.total_due: payment.loan.status='PAID'; payment.loan.save(update_fields=['status'])
        AuditLog.objects.create(actor=p, action='PAYMENT_RECORDED', object_type='Payment', object_id=str(payment.id), metadata={'amount':str(payment.amount),'receipt':receipt.number})

@api_view(['GET'])
@permission_classes([AllowAny])
def health(request): return Response({'service':'DEFA API','status':'ok'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    p=profile_for(request.user)
    return Response({'id':p.id,'user':request.user.username,'role':p.role,'verified':p.verified,'phone':p.phone})
