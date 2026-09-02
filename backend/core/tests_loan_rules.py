from decimal import Decimal
from django.test import SimpleTestCase
from rest_framework.exceptions import ValidationError
from .serializers import ApplicationSerializer, calculate_loan_fee, calculate_total_repayment


class LoanPricingTests(SimpleTestCase):
    def test_pricing_examples(self):
        self.assertEqual(calculate_loan_fee(Decimal('100000')), Decimal('12000.00'))
        self.assertEqual(calculate_total_repayment(Decimal('100000')), Decimal('112000.00'))
        self.assertEqual(calculate_loan_fee(Decimal('500000')), Decimal('60000.00'))
        self.assertEqual(calculate_total_repayment(Decimal('500000')), Decimal('560000.00'))

    def test_valid_amounts(self):
        for amount in ('100000', '200000', '300000', '1000000'):
            serializer = ApplicationSerializer(data={'amount': amount, 'purpose': 'BUSINESS'})
            try:
                serializer.is_valid(raise_exception=True)
            except ValidationError as exc:
                self.fail(f'{amount} FC devrait être accepté: {exc.detail}')

    def test_invalid_amounts(self):
        for amount in ('99999', '150000', '250000'):
            serializer = ApplicationSerializer(data={'amount': amount, 'purpose': 'BUSINESS'})
            self.assertFalse(serializer.is_valid())
            self.assertIn('amount', serializer.errors)
