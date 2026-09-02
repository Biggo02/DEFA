from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Loan

FEE_RATE = Decimal('0.12')

@receiver(pre_save, sender=Loan)
def enforce_loan_total(sender, instance, **kwargs):
    """The server is the pricing authority: total repayment is always principal + 12%."""
    if instance.principal is not None:
        principal = Decimal(instance.principal)
        instance.total_due = (principal * (Decimal('1.00') + FEE_RATE)).quantize(Decimal('0.01'))
