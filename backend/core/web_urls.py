from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .web_views import (home, simulator, sign_in, sign_up, sign_out, dashboard,
    new_application, application_detail, application_submit, loan_detail,
    operations_dashboard, application_decision, collect_payment)
from .web_extra import (page as _page, my_applications, client_profile, client_documents,
    client_notifications, client_payments, client_receipts, client_schedule,
    client_payment_detail, client_receipt_detail, client_loan_contract,
    agent_clients, agent_visits, agent_payments, agent_collection, agent_qr,
    admin_requests, admin_clients, admin_loans, admin_payments, admin_documents,
    admin_alerts, admin_audit, admin_settings, dashboard_kpis)


def page(request, title, description, area='public', eyebrow=None):
    if area != 'public' and not request.user.is_authenticated:
        return redirect('login')
    return _page(request, title, description, area, eyebrow)

client_profile = login_required(client_profile)
client_documents = login_required(client_documents)
client_notifications = login_required(client_notifications)
client_payments = login_required(client_payments)
client_receipts = login_required(client_receipts)
client_schedule = login_required(client_schedule)
client_payment_detail = login_required(client_payment_detail)
client_receipt_detail = login_required(client_receipt_detail)
client_loan_contract = login_required(client_loan_contract)
my_applications = login_required(my_applications)
agent_clients = login_required(agent_clients)
agent_visits = login_required(agent_visits)
agent_payments = login_required(agent_payments)
agent_collection = login_required(agent_collection)
agent_qr = login_required(agent_qr)
admin_requests = login_required(admin_requests)
admin_clients = login_required(admin_clients)
admin_loans = login_required(admin_loans)
admin_payments = login_required(admin_payments)
admin_documents = login_required(admin_documents)
admin_alerts = login_required(admin_alerts)
admin_audit = login_required(admin_audit)
admin_settings = login_required(admin_settings)
dashboard_kpis = login_required(dashboard_kpis)

urlpatterns = [
    path('', home, name='home'),
    path('comment-ca-marche/', lambda r: page(r, 'Comment ça marche', 'Découvrez le parcours demande → vérification → décision → contrat → remboursement.'), name='how_it_works'),
    path('simulateur/', simulator, name='simulator'),
    path('eligibilite/', lambda r: page(r, 'Conditions d’éligibilité', 'Critères, justificatifs et principes de financement responsable.'), name='eligibility'),
    path('securite/', lambda r: page(r, 'Sécurité & confiance', 'KYC, contrôle d’accès, consentement, audit et traitement responsable des données.'), name='security_public'),
    path('faq/', lambda r: page(r, 'FAQ', 'Réponses aux questions fréquentes sur les demandes et remboursements.'), name='faq'),
    path('a-propos/', lambda r: page(r, 'À propos de DEFA', 'Mission, vision et valeurs de Finance Responsable.'), name='about'),
    path('contact/', lambda r: page(r, 'Contact', 'Contactez l’équipe DEFA via les canaux configurés.'), name='contact'),
    path('connexion/', sign_in, name='login'),
    path('inscription/', sign_up, name='register'),
    path('mot-de-passe-oublie/', lambda r: page(r, 'Mot de passe oublié', 'La récupération sécurisée du compte sera effectuée sans révéler l’existence d’un compte.'), name='password_reset'),
    path('deconnexion/', sign_out, name='logout'),

    path('app/tableau-de-bord/', dashboard, name='dashboard'),
    path('app/nouvelle-demande/', new_application, name='new_application'),
    path('app/identite/', lambda r: page(r, 'Identité / KYC', 'Gérez les informations nécessaires à votre vérification.', 'client'), name='client_kyc'),
    path('app/profession/', lambda r: page(r, 'Situation professionnelle', 'Emploi, profession, ancienneté et preuves.', 'client'), name='client_profession'),
    path('app/revenus-charges/', lambda r: page(r, 'Revenus et charges', 'Déclarez vos revenus et charges pour l’analyse de capacité.', 'client'), name='client_income'),
    path('app/commerce/', lambda r: page(r, 'Commerce', 'Informations relatives à votre activité commerciale.', 'client'), name='client_business'),
    path('app/domicile/', lambda r: page(r, 'Domicile', 'Adresse et informations de résidence.', 'client'), name='client_home'),
    path('app/geolocalisation/', lambda r: page(r, 'Géolocalisation', 'Partage de localisation uniquement après consentement explicite.', 'client'), name='client_location'),
    path('app/references/', lambda r: page(r, 'Références', 'Références fournies pour votre dossier.', 'client'), name='client_references'),
    path('app/documents/', client_documents, name='client_documents'),
    path('app/resume/', my_applications, name='application_summary'),
    path('app/mes-demandes/', my_applications, name='my_applications'),
    path('app/demande/<uuid:pk>/', application_detail, name='application_detail'),
    path('app/demande/<uuid:pk>/soumettre/', application_submit, name='application_submit'),
    path('app/pret/<uuid:pk>/', loan_detail, name='loan_detail'),
    path('app/echeancier/', client_schedule, name='client_schedule'),
    path('app/paiements/', client_payments, name='client_payments'),
    path('app/paiement/<uuid:pk>/', client_payment_detail, name='client_payment_detail'),
    path('app/recus/', client_receipts, name='client_receipts'),
    path('app/recu/<str:number>/', client_receipt_detail, name='client_receipt_detail'),
    path('app/notifications/', client_notifications, name='client_notifications'),
    path('app/profil/', client_profile, name='client_profile'),
    path('app/securite/', lambda r: page(r, 'Sécurité du compte', 'Mot de passe, sessions et consentements.', 'client'), name='client_security'),
    path('app/aide/', lambda r: page(r, 'Aide', 'FAQ, assistance et aide au remboursement.', 'client'), name='client_help'),
    path('app/pret/<uuid:pk>/contrat/', client_loan_contract, name='loan_contract'),

    path('agent/', operations_dashboard, name='agent_dashboard'),
    path('agent/clients/', agent_clients, name='agent_clients'),
    path('agent/client/<int:pk>/', lambda r, pk: page(r, 'Fiche client', 'Informations strictement nécessaires à la mission.', 'agent'), name='agent_client_detail'),
    path('agent/visites/', agent_visits, name='agent_visits'),
    path('agent/visite/<int:pk>/', lambda r, pk: page(r, 'Détail de la visite', 'Résultat, notes et preuve de passage autorisée.', 'agent'), name='agent_visit_detail'),
    path('agent/carte/', lambda r: page(r, 'Carte des clients', 'Carte limitée aux clients assignés et aux permissions autorisées.', 'agent'), name='agent_map'),
    path('agent/tournee/', lambda r: page(r, 'Navigation / tournée', 'Organisation des visites et itinéraire autorisé.', 'agent'), name='agent_route'),
    path('agent/scanner/', agent_qr, name='agent_scanner'),
    path('agent/scan-resultat/', lambda r: page(r, 'Dossier après scan', 'Informations minimales du prêt après authentification.', 'agent'), name='agent_scan_result'),
    path('agent/paiement/', lambda r: page(r, 'Enregistrer un paiement', 'Sélectionnez un prêt autorisé puis enregistrez l’encaissement.', 'agent'), name='agent_payment'),
    path('agent/paiement/confirmation/', lambda r: page(r, 'Confirmation paiement', 'Confirmation et nouveau solde après encaissement.', 'agent'), name='agent_payment_confirmation'),
    path('agent/recu/', lambda r: page(r, 'Reçu généré', 'Preuve de transaction générée après paiement.', 'agent'), name='agent_receipt'),
    path('agent/paiements/', agent_payments, name='agent_payments'),
    path('agent/recouvrement/', agent_collection, name='agent_collection'),
    path('agent/rapport/', lambda r: page(r, 'Rapport quotidien', 'Visites, paiements, incidents et commentaires.', 'agent'), name='agent_report'),
    path('agent/profil/', lambda r: page(r, 'Profil agent', 'Profil, zone, statut et paramètres.', 'agent'), name='agent_profile'),

    path('admin-dashboard/', dashboard_kpis, name='admin_dashboard'),
    path('admin/demandes/', admin_requests, name='admin_requests'),
    path('admin/demande/<uuid:pk>/', lambda r, pk: page(r, 'Analyse d’une demande', 'Vue 360° du dossier et des éléments nécessaires à la décision.', 'admin'), name='admin_application_detail'),
    path('admin/scoring/', lambda r: page(r, 'Score de crédit', 'Score indicatif, facteurs, capacité estimée et alertes.', 'admin'), name='admin_scoring'),
    path('admin/kyc/', admin_documents, name='admin_kyc'),
    path('admin/documents/', admin_documents, name='admin_documents'),
    path('admin/clients/', admin_clients, name='admin_clients'),
    path('admin/client/<int:pk>/', lambda r, pk: page(r, 'Fiche client complète', 'Vue 360° sécurisée du client.', 'admin'), name='admin_client_detail'),
    path('admin/prets/', admin_loans, name='admin_loans'),
    path('admin/pret/<uuid:pk>/', lambda r, pk: page(r, 'Détail d’un prêt', 'Contrat, échéancier, paiements, retards, QR et audit.', 'admin'), name='admin_loan_detail'),
    path('admin/echeanciers/', lambda r: page(r, 'Échéanciers', 'Consultation et contrôle des échéanciers.', 'admin'), name='admin_schedules'),
    path('admin/paiements/', admin_payments, name='admin_payments'),
    path('admin/recouvrement/', lambda r: page(r, 'Recouvrement', 'Portefeuille en retard, priorités et affectations.', 'admin'), name='admin_collection'),
    path('admin/agents/', lambda r: page(r, 'Agents', 'Agents, statut, zone et performance.', 'admin'), name='admin_agents'),
    path('admin/visites/', lambda r: page(r, 'Visites terrain', 'Toutes les visites, résultats et agents.', 'admin'), name='admin_visits'),
    path('admin/carte/', lambda r: page(r, 'Carte générale', 'Carte soumise aux permissions et règles de confidentialité.', 'admin'), name='admin_map'),
    path('admin/alertes/', admin_alerts, name='admin_alerts'),
    path('admin/parametres-scoring/', lambda r: page(r, 'Scoring / paramètres', 'Règles, pondérations et seuils configurables.', 'admin'), name='admin_scoring_settings'),
    path('admin/notifications/', lambda r: page(r, 'Notifications', 'Événements, modèles et historique.', 'admin'), name='admin_notifications'),
    path('admin/rapports/', lambda r: page(r, 'Rapports', 'Rapports financiers, risque, recouvrement et activité.', 'admin'), name='admin_reports'),
    path('admin/audit/', admin_audit, name='admin_audit'),
    path('admin/utilisateurs/', lambda r: page(r, 'Utilisateurs', 'Comptes, rôles, permissions et sécurité.', 'admin'), name='admin_users'),
    path('admin/parametres/', admin_settings, name='admin_settings'),
    path('admin/securite/', lambda r: page(r, 'Sécurité', 'Politiques, accès et événements suspects.', 'admin'), name='admin_security'),

    path('etat/demande-en-cours/', lambda r: page(r, 'Demande en cours', 'Votre dossier suit le processus DEFA.'), name='state_pending'),
    path('etat/informations-manquantes/', lambda r: page(r, 'Informations manquantes', 'Complétez les éléments demandés avant la poursuite du dossier.'), name='state_missing'),
    path('etat/approuvee/', lambda r: page(r, 'Demande approuvée', 'Votre demande est approuvée sous réserve des conditions et formalités applicables.'), name='state_approved'),
    path('etat/refusee/', lambda r: page(r, 'Demande refusée', 'Votre demande n’a pas été retenue. Consultez l’aide pour les prochaines étapes.'), name='state_rejected'),
    path('etat/pret-en-retard/', lambda r: page(r, 'Prêt en retard', 'Consultez les échéances concernées et contactez DEFA.'), name='state_late'),
    path('etat/paiement-partiel/', lambda r: page(r, 'Paiement partiel', 'Le paiement reçu a été appliqué au solde de l’échéance.'), name='state_partial'),
    path('etat/pret-rembourse/', lambda r: page(r, 'Prêt remboursé', 'Le remboursement total est enregistré.'), name='state_paid'),
    path('etat/compte-suspendu/', lambda r: page(r, 'Compte suspendu', 'L’accès est temporairement limité. Contactez DEFA pour assistance.'), name='state_suspended'),
]
