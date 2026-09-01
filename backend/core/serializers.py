from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Address, Employment, Business, Reference, LoanApplication, Loan, Installment, Payment, PaymentReceipt

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
    class Meta:
        model = LoanApplication
        fields = '__all__'
        read_only_fields = ['id','profile','score','risk_class','status','submitted_at','created_at','updated_at']

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
