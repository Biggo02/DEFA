from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile, Loan, Payment, PaymentReceipt, AuditLog, Notification
from .serializers import PaymentSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def collect_payment(request):
    try:
        p=Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({'detail':'Profil introuvable.'},status=404)
    if p.role not in ('ADMIN','AGENT'):
        return Response({'detail':'Seuls les agents autorisés peuvent enregistrer un encaissement.'},status=403)
    loan=get_object_or_404(Loan,pk=request.data.get('loan'))
    try: amount=Decimal(str(request.data.get('amount')))
    except Exception: return Response({'detail':'Montant invalide.'},status=400)
    if amount<=0: return Response({'detail':'Le montant doit être positif.'},status=400)
    with transaction.atomic():
        loan=Loan.objects.select_for_update().get(pk=loan.pk)
        paid=loan.payments.aggregate(v=Sum('amount'))['v'] or Decimal('0')
        remaining=loan.total_due-paid
        if amount>remaining: return Response({'detail':'Le montant dépasse le solde du prêt.','remaining':str(remaining)},status=400)
        payment=Payment.objects.create(loan=loan,amount=amount,method=request.data.get('method','CASH'),client_confirmed=bool(request.data.get('client_confirmed',False)),agent=p)
        left=amount
        for inst in loan.installments.select_for_update().order_by('number'):
            room=max(Decimal('0'),inst.amount_due-inst.amount_paid)
            applied=min(room,left)
            if applied:
                inst.amount_paid+=applied
                inst.status='PAID' if inst.amount_paid>=inst.amount_due else 'PARTIAL'
                inst.save(update_fields=['amount_paid','status'])
                if payment.installment_id is None: payment.installment=inst
                left-=applied
            if left<=0: break
        payment.save(update_fields=['installment'])
        receipt=PaymentReceipt.objects.create(payment=payment,number=f'DEFA-{timezone.now():%Y%m%d}-{str(payment.id)[:8].upper()}')
        new_total=paid+amount
        if new_total>=loan.total_due:
            loan.status='PAID'; loan.save(update_fields=['status'])
        AuditLog.objects.create(actor=p,action='PAYMENT_RECORDED',object_type='Payment',object_id=str(payment.id),metadata={'amount':str(amount),'receipt':receipt.number})
        Notification.objects.create(profile=loan.profile,title='Paiement enregistré',message=f'Paiement de {amount} enregistré. Reçu {receipt.number}.',kind='PAYMENT')
    return Response({'payment':PaymentSerializer(payment).data,'receipt':{'number':receipt.number},'remaining':str(max(Decimal('0'),loan.total_due-new_total))},status=201)
