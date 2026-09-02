from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Address, Employment, Business, Reference, LoanApplication, Loan, Installment, Payment, PaymentReceipt

MIN_LOAN_AMOUNT = Decimal('100000')
LOAN_STEP = Decimal('100000')
FEE_RATE = Decimal('0.12')


def calculate_loan_fee(amount):
    return (Decimal(amount) * FEE_RATE).quantize(Decimal('0.01'))


def calculate_total_repayment(amount):
    amount = Decimal(amount)
    return (amount + calculate_loan_fee(amount)).quantize(Decimal('0.01'))

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','role','phone','national_id','photo','verified']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['profile','verified']

class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = '__all__'
        read_only_fields = ['profile','verified']

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'
        read_only_fields = ['profile','verified']

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'
        read_only_fields = ['profile','verified']

class ApplicationSerializer(serializers.ModelSerializer):
    fee = serializers.SerializerMethodField()
    total_repayment = serializers.SerializerMethodField()

    class Meta:
        model = LoanApplication
        fields = '__all__'
        read_only_fields = ['id','profile','score','risk_class','status','submitted_at','created_at','updated_at','fee','total_repayment']

    def validate_amount(self, value):
        if value < MIN_LOAN_AMOUNT:
            raise serializers.ValidationError('Le montant minimum du prêt est de 100 000 FC.')
        if value % LOAN_STEP != 0:
            raise serializers.ValidationError('Le montant doit être un multiple de 100 000 FC.')
        return value

    def get_fee(self, obj):
        return calculate_loan_fee(obj.amount)

    def get_total_repayment(self, obj):
        return calculate_total_repayment(obj.amount)

class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id','loan','installment','agent','amount','method','client_confirmed','created_at']
        read_only_fields = ['id','agent','created_at']

class ReceiptSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    class Meta:
        model = PaymentReceipt
        fields = ['number','payment','created_at']

class LoanSerializer(serializers.ModelSerializer):
    installments = InstallmentSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    class Meta:
        model = Loan
        fields = ['id','application','profile','principal','total_due','disbursed_at','status','qr_token','created_at','installments','payments']
        read_only_fields = fields
