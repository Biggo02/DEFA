from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from core.models import Profile, Loan, LoanApplication

class DEFAWebPortalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='client_test', password='StrongPass123!', first_name='Client')
        self.profile = Profile.objects.create(user=self.user, phone='+243000000000')

    def test_public_routes(self):
        for name in ('home','how_it_works','simulator','eligibility','security_public','faq','about','contact','login','register','password_reset'):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)

    def test_simulator_accepts_only_hundred_thousand_steps(self):
        response = self.client.post(reverse('simulator'), {'amount':'300000'})
        self.assertContains(response, '36,000')
        self.assertContains(response, '336,000')
        invalid = self.client.post(reverse('simulator'), {'amount':'350000'})
        self.assertContains(invalid, 'Montant invalide')

    def test_client_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_loan_total_is_authoritative(self):
        app = LoanApplication.objects.create(profile=self.profile, amount=Decimal('500000'), purpose='BUSINESS')
        loan = Loan.objects.create(application=app, profile=self.profile, principal=Decimal('500000'), total_due=Decimal('999999'))
        loan.refresh_from_db()
        self.assertEqual(loan.total_due, Decimal('560000.00'))
