from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, AddressViewSet, EmploymentViewSet, BusinessViewSet, ReferenceViewSet, ApplicationViewSet, LoanViewSet, PaymentViewSet, health, me
from .auth import register, login
from .api_extra import (DocumentViewSet, AssignmentViewSet, VerificationVisitViewSet,
    LocationConsentViewSet, LocationRecordViewSet, ContractViewSet, CollectionViewSet,
    NotificationViewSet, FraudViewSet, dashboard, qr_lookup)

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profile')
router.register('addresses', AddressViewSet, basename='address')
router.register('employment', EmploymentViewSet, basename='employment')
router.register('businesses', BusinessViewSet, basename='business')
router.register('references', ReferenceViewSet, basename='reference')
router.register('applications', ApplicationViewSet, basename='application')
router.register('loans', LoanViewSet, basename='loan')
router.register('payments', PaymentViewSet, basename='payment')
router.register('documents', DocumentViewSet, basename='document')
router.register('assignments', AssignmentViewSet, basename='assignment')
router.register('verification-visits', VerificationVisitViewSet, basename='verification-visit')
router.register('location-consents', LocationConsentViewSet, basename='location-consent')
router.register('locations', LocationRecordViewSet, basename='location')
router.register('contracts', ContractViewSet, basename='contract')
router.register('collections', CollectionViewSet, basename='collection')
router.register('notifications', NotificationViewSet, basename='notification')
router.register('fraud-alerts', FraudViewSet, basename='fraud')

urlpatterns = [
    path('health/', health), path('me/', me), path('register/', register), path('login/', login),
    path('dashboard/', dashboard), path('qr/<uuid:token>/', qr_lookup), path('', include(router.urls))
]
