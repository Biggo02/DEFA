from django.contrib import admin
from .models import *

MODELS = [
    Profile, Address, Employment, Business, Reference, UploadedDocument,
    LoanApplication, VerificationVisit, AgentAssignment, LocationConsent,
    LocationRecord, Loan, Installment, Contract, Payment, PaymentReceipt,
    CollectionVisit, Notification, FraudAlert, SystemSetting, Consent, AuditLog,
]
for model in MODELS:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
