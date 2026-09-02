from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import (
    Address, Business, Employment, Loan, LoanApplication, Payment, PaymentReceipt,
    Profile, Reference, UploadedDocument, LocationConsent, LocationRecord,
    Installment, Contract, Notification, AuditLog,
)

MIN_LOAN = Decimal('100000')
STEP_LOAN = Decimal('100000')
FEE_RATE = Decimal('0.12')


def loan_values(amount):
    amount = Decimal(str(amount))
    fee = (amount * FEE_RATE).quantize(Decimal('0.01'))
    return fee, amount + fee


def valid_loan_amount(amount):
    return amount >= MIN_LOAN and amount % STEP_LOAN == 0


def home(request):
    return render(request, 'home.html')


def simulator(request):
    raw = request.POST.get('amount') or request.GET.get('amount') or '100000'
    try:
        amount = Decimal(raw)
    except (InvalidOperation, TypeError):
        amount = MIN_LOAN
    valid = valid_loan_amount(amount)
    fee, total = loan_values(amount) if valid else (Decimal('0'), Decimal('0'))
    return render(request, 'simulator.html', {
        'amount': amount, 'fee': fee, 'total': total, 'valid': valid,
        'min_loan': MIN_LOAN, 'step_loan': STEP_LOAN,
    })


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Identifiants invalides.')
    return render(request, 'login.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        if not username or len(password) < 8 or not first_name or not phone:
            messages.error(request, 'Remplissez les champs obligatoires. Le mot de passe doit contenir au moins 8 caractères.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ce compte existe déjà.')
        else:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            Profile.objects.create(user=user, phone=phone)
            login(request, user)
            return redirect('dashboard')
    return render(request, 'register.html')


def sign_out(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.role in ('ADMIN', 'ANALYST', 'AGENT'):
        return redirect('operations_dashboard')
    applications = LoanApplication.objects.filter(profile=profile).order_by('-created_at')
    loans = Loan.objects.filter(profile=profile).order_by('-created_at')
    payments = Payment.objects.filter(loan__profile=profile).select_related('loan').order_by('-created_at')[:10]
    notifications = Notification.objects.filter(profile=profile).order_by('-created_at')[:8]
    return render(request, 'dashboard.html', {
        'profile': profile, 'applications': applications, 'loans': loans,
        'payments': payments, 'notifications': notifications,
    })


@login_required
def new_application(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            income = Decimal(request.POST.get('monthly_income', '0') or '0')
            expenses = Decimal(request.POST.get('monthly_expenses', '0') or '0')
            duration = int(request.POST.get('duration_days', '30'))
            if not valid_loan_amount(amount):
                raise ValidationError('Le montant doit être au minimum de 100 000 FC et uniquement par tranches de 100 000 FC.')
            if income < 0 or expenses < 0:
                raise ValidationError('Les revenus et charges ne peuvent pas être négatifs.')
            if duration < 7:
                raise ValidationError('La durée minimale est de 7 jours.')
            with transaction.atomic():
                app = LoanApplication.objects.create(
                    profile=profile, amount=amount, duration_days=duration,
                    frequency=request.POST.get('frequency', 'WEEKLY'),
                    purpose=request.POST.get('purpose', 'OTHER'),
                    purpose_detail=request.POST.get('purpose_detail', '').strip(),
                    monthly_income=income, monthly_expenses=expenses,
                )
                _save_client_dossier(request, profile, app)
            messages.success(request, 'Demande enregistrée. Vérifiez le dossier puis cliquez sur « Soumettre » pour lancer l’analyse.')
            return redirect('application_detail', app.id)
        except (ValidationError, InvalidOperation, ValueError) as exc:
            messages.error(request, exc.message if hasattr(exc, 'message') else str(exc))
    return render(request, 'application_form.html', {'min_loan': MIN_LOAN, 'step_loan': STEP_LOAN, 'profile': profile})


def _save_client_dossier(request, profile, app):
    profile.national_id = request.POST.get('national_id', profile.national_id).strip()
    profile.save(update_fields=['national_id'])
    Employment.objects.update_or_create(profile=profile, defaults={
        'status': request.POST.get('employment_status', 'EMPLOYED'),
        'employer': request.POST.get('employer', '').strip(),
        'position': request.POST.get('position', '').strip(),
        'monthly_income': app.monthly_income,
        'years_active': Decimal(request.POST.get('employment_years', '0') or '0'),
    })
    Address.objects.update_or_create(profile=profile, kind='HOME', defaults={
        'address': request.POST.get('home_address', '').strip(),
        'city': request.POST.get('city', '').strip(),
        'neighborhood': request.POST.get('neighborhood', '').strip(),
    })
    business_name = request.POST.get('business_name', '').strip()
    business_activity = request.POST.get('business_activity', '').strip()
    if business_name and business_activity:
        Business.objects.create(profile=profile, name=business_name, activity=business_activity,
                                years_active=Decimal(request.POST.get('business_years', '0') or '0'),
                                monthly_revenue=Decimal(request.POST.get('business_revenue', '0') or '0'),
                                monthly_expenses=Decimal(request.POST.get('business_expenses', '0') or '0'))
    names = request.POST.getlist('reference_name')
    relations = request.POST.getlist('reference_relationship')
    phones = request.POST.getlist('reference_phone')
    for name, relation, phone in zip(names, relations, phones):
        if name.strip() and phone.strip():
            Reference.objects.create(profile=profile, name=name.strip(), relationship=relation.strip(), phone=phone.strip())
    consent = request.POST.get('location_consent') == 'on'
    if consent:
        LocationConsent.objects.create(profile=profile, purpose='Vérification du dossier de prêt', granted=True, granted_at=timezone.now())
    for field, kind in (('document_id', 'NATIONAL_ID'), ('document_address', 'ADDRESS'), ('document_income', 'INCOME'), ('document_business', 'BUSINESS')):
        f = request.FILES.get(field)
        if f:
            UploadedDocument.objects.create(profile=profile, document_type=kind, file=f)


@login_required
def application_submit(request, pk):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    app = get_object_or_404(LoanApplication, pk=pk, profile=profile)
    if request.method != 'POST' or app.status not in ('DRAFT', 'MORE_INFO'):
        return redirect('application_detail', pk=app.id)
    missing = []
    if not profile.national_id: missing.append('pièce d’identité')
    if not profile.documents.filter(document_type='NATIONAL_ID').exists(): missing.append('document d’identité')
    if not (app.monthly_income > 0 or profile.businesses.exists()): missing.append('source de revenus ou commerce')
    if profile.references.count() < 2: missing.append('au moins deux références')
    if missing:
        app.status = 'MORE_INFO'; app.save(update_fields=['status', 'updated_at'])
        messages.error(request, 'Dossier incomplet : ' + ', '.join(missing) + '.')
        return redirect('application_detail', pk=app.id)
    score = 0
    if profile.national_id and profile.verified: score += 15
    employment = getattr(profile, 'employment', None)
    if employment and employment.monthly_income > 0: score += 20
    if employment and employment.years_active >= 1: score += 10
    if profile.businesses.filter(verified=True).exists(): score += 15
    disposable = max(Decimal('0'), app.monthly_income - app.monthly_expenses)
    if disposable > 0: score += 20
    if app.amount <= max(Decimal('1'), disposable * 2): score += 15
    if profile.references.filter(verified=True).count() >= 2: score += 10
    if profile.documents.filter(document_type='NATIONAL_ID', status='VERIFIED').exists(): score += 5
    score = min(score, 100)
    risk = 'A' if score >= 80 else 'B' if score >= 65 else 'C' if score >= 50 else 'D'
    app.score, app.risk_class, app.status, app.submitted_at = score, risk, 'VERIFYING', timezone.now()
    app.save(update_fields=['score', 'risk_class', 'status', 'submitted_at', 'updated_at'])
    AuditLog.objects.create(actor=profile, action='APPLICATION_SUBMITTED', object_type='LoanApplication', object_id=str(app.id), metadata={'score': score, 'risk': risk})
    messages.success(request, 'Votre demande est soumise. DEFA peut maintenant procéder aux vérifications.')
    return redirect('application_detail', pk=app.id)


@login_required
def application_detail(request, pk):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    app = get_object_or_404(LoanApplication, pk=pk, profile=profile)
    fee, total = loan_values(app.amount)
    return render(request, 'application_detail.html', {
        'app': app, 'fee': fee, 'total': total,
        'documents': profile.documents.order_by('-created_at'),
        'references': profile.references.order_by('-id'),
        'address': profile.addresses.filter(kind='HOME').first(),
    })


@login_required
def loan_detail(request, pk):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    loan = get_object_or_404(Loan, pk=pk, profile=profile)
    paid = loan.payments.aggregate(v=Sum('amount'))['v'] or Decimal('0')
    return render(request, 'loan_detail.html', {'loan': loan, 'paid': paid, 'remaining': max(Decimal('0'), loan.total_due-paid)})


@login_required
def operations_dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.role not in ('ADMIN', 'ANALYST', 'AGENT'):
        return redirect('dashboard')
    applications = LoanApplication.objects.select_related('profile__user').order_by('-created_at')
    if profile.role == 'AGENT':
        applications = applications.filter(status__in=('VERIFYING', 'APPROVED'))
    loans = Loan.objects.select_related('profile__user').order_by('-created_at')
    payments = Payment.objects.select_related('loan__profile__user').order_by('-created_at')[:20]
    return render(request, 'operations.html', {'profile': profile, 'applications': applications[:50], 'loans': loans[:50], 'payments': payments})


@login_required
def application_decision(request, pk):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.role not in ('ADMIN', 'ANALYST') or request.method != 'POST':
        return redirect('operations_dashboard')
    app = get_object_or_404(LoanApplication, pk=pk)
    decision = request.POST.get('decision')
    if decision not in ('APPROVED', 'REJECTED', 'MORE_INFO'):
        messages.error(request, 'Décision invalide.')
        return redirect('operations_dashboard')
    if decision == 'APPROVED' and app.score < 50:
        messages.error(request, 'Score inférieur à 50 : validation manuelle renforcée requise.')
        return redirect('operations_dashboard')
    if decision == 'APPROVED':
        fee, total = loan_values(app.amount)
        with transaction.atomic():
            app.status = 'APPROVED'; app.save(update_fields=['status', 'updated_at'])
            loan, created = Loan.objects.get_or_create(application=app, defaults={'profile': app.profile, 'principal': app.amount, 'total_due': total})
            if created:
                count = max(1, app.duration_days // (30 if app.frequency == 'MONTHLY' else 7))
                installment = (total / count).quantize(Decimal('0.01'))
                remainder = total - installment * count
                start = timezone.localdate() + timezone.timedelta(days=30 if app.frequency == 'MONTHLY' else 7)
                for n in range(1, count + 1):
                    amount = installment + (remainder if n == count else Decimal('0'))
                    due = start + timezone.timedelta(days=(n-1) * (30 if app.frequency == 'MONTHLY' else 7))
                    Installment.objects.create(loan=loan, number=n, due_date=due, amount_due=amount)
                Contract.objects.create(loan=loan, status='PENDING', terms={'principal': str(app.amount), 'fee': str(fee), 'total_due': str(total), 'duration_days': app.duration_days, 'frequency': app.frequency})
                Notification.objects.create(profile=app.profile, title='Demande approuvée', message='Votre demande DEFA est approuvée. Consultez votre contrat.', kind='LOAN_APPROVED')
    else:
        app.status = decision; app.save(update_fields=['status', 'updated_at'])
        Notification.objects.create(profile=app.profile, title='Mise à jour de votre demande', message='Votre dossier DEFA a été mis à jour.', kind=f'APPLICATION_{decision}')
    AuditLog.objects.create(actor=profile, action=f'APPLICATION_{decision}', object_type='LoanApplication', object_id=str(app.id))
    messages.success(request, 'Décision enregistrée.')
    return redirect('operations_dashboard')


@login_required
def collect_payment(request, pk):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.role not in ('ADMIN', 'AGENT') or request.method != 'POST':
        return redirect('operations_dashboard')
    loan = get_object_or_404(Loan, pk=pk)
    try:
        amount = Decimal(request.POST.get('amount', '0'))
        if amount <= 0: raise ValidationError('Le paiement doit être supérieur à 0.')
        with transaction.atomic():
            loan = Loan.objects.select_for_update().get(pk=loan.pk)
            paid = loan.payments.aggregate(v=Sum('amount'))['v'] or Decimal('0')
            remaining = loan.total_due - paid
            if amount > remaining: raise ValidationError(f'Solde restant : {remaining} FC.')
            payment = Payment.objects.create(loan=loan, amount=amount, method='CASH', agent=profile, client_confirmed=True)
            left = amount
            for inst in loan.installments.select_for_update().order_by('number'):
                room = max(Decimal('0'), inst.amount_due - inst.amount_paid)
                applied = min(room, left)
                if applied:
                    inst.amount_paid += applied
                    inst.status = 'PAID' if inst.amount_paid >= inst.amount_due else 'PARTIAL'
                    inst.save(update_fields=['amount_paid', 'status'])
                    left -= applied
                if left <= 0: break
            receipt = PaymentReceipt.objects.create(payment=payment, number=f'DEFA-{timezone.now():%Y%m%d}-{str(payment.id)[:8].upper()}')
            if paid + amount >= loan.total_due:
                loan.status = 'PAID'; loan.save(update_fields=['status'])
            Notification.objects.create(profile=loan.profile, title='Paiement enregistré', message=f'Paiement de {amount} FC reçu. Reçu {receipt.number}.', kind='PAYMENT')
            AuditLog.objects.create(actor=profile, action='PAYMENT_RECORDED', object_type='Payment', object_id=str(payment.id), metadata={'amount': str(amount), 'receipt': receipt.number})
        messages.success(request, f'Paiement enregistré. Reçu : {receipt.number}')
    except (ValidationError, InvalidOperation) as exc:
        messages.error(request, exc.message if hasattr(exc, 'message') else str(exc))
    return redirect('operations_dashboard')
