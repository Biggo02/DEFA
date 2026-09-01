from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, AddressViewSet, EmploymentViewSet, BusinessViewSet, ReferenceViewSet, ApplicationViewSet, LoanViewSet, PaymentViewSet, health, me
from .auth import register, login

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profile')
router.register('addresses', AddressViewSet, basename='address')
router.register('employment', EmploymentViewSet, basename='employment')
router.register('businesses', BusinessViewSet, basename='business')
router.register('references', ReferenceViewSet, basename='reference')
router.register('applications', ApplicationViewSet, basename='application')
router.register('loans', LoanViewSet, basename='loan')
router.register('payments', PaymentViewSet, basename='payment')
urlpatterns = [path('health/', health), path('me/', me), path('auth/register/', register), path('auth/login/', login), path('', include(router.urls))]
