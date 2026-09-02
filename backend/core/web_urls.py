from django.urls import path
from .web_views import (
    home, simulator, sign_in, sign_up, sign_out, dashboard,
    new_application, application_detail, application_submit,
    loan_detail, operations_dashboard, application_decision, collect_payment,
)

urlpatterns = [
    path('', home, name='home'),
    path('simulateur/', simulator, name='simulator'),
    path('connexion/', sign_in, name='login'),
    path('inscription/', sign_up, name='register'),
    path('deconnexion/', sign_out, name='logout'),
    path('app/tableau-de-bord/', dashboard, name='dashboard'),
    path('app/nouvelle-demande/', new_application, name='new_application'),
    path('app/demande/<uuid:pk>/', application_detail, name='application_detail'),
    path('app/demande/<uuid:pk>/soumettre/', application_submit, name='application_submit'),
    path('app/pret/<uuid:pk>/', loan_detail, name='loan_detail'),
    path('operations/', operations_dashboard, name='operations_dashboard'),
    path('operations/demande/<uuid:pk>/decision/', application_decision, name='application_decision'),
    path('operations/pret/<uuid:pk>/paiement/', collect_payment, name='collect_payment'),
]
