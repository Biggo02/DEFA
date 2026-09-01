from django.contrib import admin
from .models import *

for model in [Profile, Address, Employment, Business, Reference, LoanApplication, VerificationVisit, Loan, Installment, Payment, PaymentReceipt, Consent, AuditLog]:
    admin.site.register(model)
