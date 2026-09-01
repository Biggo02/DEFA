import uuid
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = [('CLIENT','Client'),('AGENT','Agent'),('ANALYST','Analyste'),('ADMIN','Administrateur')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CLIENT')
    phone = models.CharField(max_length=30, blank=True)
    national_id = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    KIND = [('HOME','Domicile'),('BUSINESS','Commerce')]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='addresses')
    kind = models.CharField(max_length=20, choices=KIND)
    address = models.TextField()
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    verified = models.BooleanField(default=False)

class Employment(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='employment')
    status = models.CharField(max_length=40, default='EMPLOYED')
    employer = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=150, blank=True)
    monthly_income = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    years_active = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    verified = models.BooleanField(default=False)

class Business(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=200)
    activity = models.CharField(max_length=200)
    years_active = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    monthly_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    monthly_expenses = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    verified = models.BooleanField(default=False)

class Reference(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='references')
    name = models.CharField(max_length=150)
    relationship = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    verified = models.BooleanField(default=False)

class LoanApplication(models.Model):
    STATUS = [('DRAFT','Brouillon'),('SUBMITTED','Soumise'),('VERIFYING','En vérification'),('REVIEW','Analyse'),('MORE_INFO','Informations complémentaires'),('APPROVED','Approuvée'),('REJECTED','Refusée')]
    PURPOSES = [('BUSINESS','Commerce'),('STOCK','Stock'),('EQUIPMENT','Équipement'),('PERSONAL','Personnel'),('EMERGENCY','Urgence'),('OTHER','Autre')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='applications')
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('1'))])
    duration_days = models.PositiveIntegerField(default=30)
    frequency = models.CharField(max_length=20, default='WEEKLY')
    purpose = models.CharField(max_length=30, choices=PURPOSES)
    purpose_detail = models.TextField(blank=True)
    monthly_income = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    monthly_expenses = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    score = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    risk_class = models.CharField(max_length=1, default='D')
    status = models.CharField(max_length=20, choices=STATUS, default='DRAFT')
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class VerificationVisit(models.Model):
    RESULT = [('PENDING','En attente'),('VERIFIED','Vérifié'),('REVIEW','À revoir'),('FAILED','Impossible')]
    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='visits')
    agent = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='visits')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    visited_at = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=20, choices=RESULT, default='PENDING')
    notes = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

class Loan(models.Model):
    STATUS = [('ACTIVE','Actif'),('LATE','En retard'),('PAID','Remboursé'),('CANCELLED','Annulé')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.OneToOneField(LoanApplication, on_delete=models.PROTECT, related_name='loan')
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='loans')
    principal = models.DecimalField(max_digits=14, decimal_places=2)
    total_due = models.DecimalField(max_digits=14, decimal_places=2)
    disbursed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='ACTIVE')
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Installment(models.Model):
    STATUS = [('UPCOMING','À venir'),('DUE','À payer'),('PARTIAL','Partielle'),('PAID','Payée'),('LATE','En retard')]
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='installments')
    number = models.PositiveIntegerField()
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=14, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='UPCOMING')
    class Meta:
        unique_together = ('loan','number')
        ordering = ['number']

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT, related_name='payments')
    installment = models.ForeignKey(Installment, on_delete=models.PROTECT, related_name='payments', null=True, blank=True)
    agent = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='payments_collected', null=True, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    method = models.CharField(max_length=30, default='CASH')
    client_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class PaymentReceipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.PROTECT, related_name='receipt')
    number = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Consent(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='consents')
    kind = models.CharField(max_length=60)
    granted = models.BooleanField(default=False)
    granted_at = models.DateTimeField(null=True, blank=True)
    version = models.CharField(max_length=20, default='1.0')

class AuditLog(models.Model):
    actor = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)
    action = models.CharField(max_length=120)
    object_type = models.CharField(max_length=80, blank=True)
    object_id = models.CharField(max_length=100, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
