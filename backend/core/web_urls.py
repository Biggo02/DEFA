from django.urls import path
from .web_views import home, simulator, sign_in, sign_up, sign_out, dashboard, new_application, application_detail

urlpatterns = [
    path('', home, name='home'),
    path('simulateur/', simulator, name='simulator'),
    path('connexion/', sign_in, name='login'),
    path('inscription/', sign_up, name='register'),
    path('deconnexion/', sign_out, name='logout'),
    path('app/tableau-de-bord/', dashboard, name='dashboard'),
    path('app/nouvelle-demande/', new_application, name='new_application'),
    path('app/demande/<uuid:pk>/', application_detail, name='application_detail'),
]
