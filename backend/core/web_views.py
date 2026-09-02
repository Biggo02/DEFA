from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Profile, LoanApplication, Loan, Payment

MIN_LOAN = Decimal('100000')
STEP_LOAN = Decimal('100000')
FEE_RATE = Decimal('0.12')


def loan_values(amount):
    amount = Decimal(str(amount))
    fee = (amount * FEE_RATE).quantize(Decimal('0.01'))
    return fee, amount + fee


def home(request):
    return render(request, 'home.html')


def simulator(request):
    raw = request.POST.get('amount') or request.GET.get('amount') or '100000'
    try:
        amount = Decimal(raw)
    except Exception:
        amount = MIN_LOAN
    valid = amount >= MIN_LOAN and amount % STEP_LOAN == 0
    fee, total = loan_values(amount if valid else MIN_LOAN)
    return render(request, 'simulator.html', {'amount': amount, 'fee': fee, 'total': total, 'valid': valid})


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
    applications = LoanApplication.objects.filter(profile=profile).order_by('-created_at')
    loans = Loan.objects.filter(profile=profile).order_by('-created_at')
    payments = Payment.objects.filter(loan__profile=profile).order_by('-created_at')[:10]
    return render(request, 'dashboard.html', {'profile': profile, 'applications': applications, 'loans': loans, 'payments': payments})


@login_required
def new_application(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            if amount < MIN_LOAN or amount % STEP_LOAN != 0:
                raise ValueError('Le montant doit être au minimum de 100 000 FC et par tranches de 100 000 FC.')
            income = Decimal(request.POST.get('monthly_income', '0') or '0')
            expenses = Decimal(request.POST.get('monthly_expenses', '0') or '0')
            if income < 0 or expenses < 0:
                raise ValueError('Les revenus et charges ne peuvent pas être négatifs.')
            profile, _ = Profile.objects.get_or_create(user=request.user)
            with transaction.atomic():
                app = LoanApplication.objects.create(profile=profile, amount=amount, duration_days=int(request.POST.get('duration_days', '30')), frequency=request.POST.get('frequency', 'WEEKLY'), purpose=request.POST.get('purpose', 'OTHER'), purpose_detail=request.POST.get('purpose_detail', ''), monthly_income=income, monthly_expenses=expenses)
            messages.success(request, 'Votre demande a été enregistrée. Elle sera analysée par DEFA.')
            return redirect('application_detail', app.id)
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, 'application_form.html', {'min_loan': MIN_LOAN, 'step_loan': STEP_LOAN})


@login_required
def application_detail(request, pk):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    app = get_object_or_404(LoanApplication, pk=pk, profile=profile)
    fee, total = loan_values(app.amount)
    return render(request, 'application_detail.html', {'app': app, 'fee': fee, 'total': total})
