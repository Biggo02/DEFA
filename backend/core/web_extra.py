from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from .models import (Profile, LoanApplication, Loan, Installment, Payment,
    PaymentReceipt, UploadedDocument, Reference, Address, Employment, Business,
    VerificationVisit, AgentAssignment, CollectionVisit, Notification, FraudAlert,
    Contract, AuditLog, SystemSetting)


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped(request, *args, **kwargs):
            profile, _ = Profile.objects.get_or_create(user=request.user)
            if profile.role not in roles:
                return redirect('dashboard')
            return view(request, profile, *args, **kwargs)
        return wrapped
    return decorator


def public_page(request, title, eyebrow, description, cards=None):
    return render(request, 'portal_page.html', {
        'page_title': title, 'eyebrow': eyebrow, 'page_description': description,
        'cards': cards or [], 'public_page': True,
    })


def client_page(request, title, description, cards=None):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'portal_page.html', {
        'page_title': title, 'eyebrow': 'ESPACE CLIENT', 'page_description': description,
        'cards': cards or [], 'profile': profile, 'client_page': True,
    })


def staff_page(request, title, description, cards=None, role='STAFF'):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.role not in (('AGENT',) if role == 'AGENT' else ('ADMIN','ANALYST') if role == 'ADMIN' else ('AGENT','ADMIN','ANALYST')):
        return redirect('dashboard')
    return render(request, 'portal_page.html', {
        'page_title': title, 'eyebrow': 'ESPACE ' + profile.get_role_display().upper(),
        'page_description': description, 'cards': cards or [], 'profile': profile,
        'staff_page': True,
    })


def my_applications(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    apps = LoanApplication.objects.filter(profile=profile).order_by('-created_at')
    cards = [{'title': 'Mes demandes', 'value': apps.count(), 'text': 'Dossiers enregistrés', 'items': [f'{a.amount:,.0f} FC — {a.get_status_display()}' for a in apps[:10]]}]
    return client_page(request, 'Mes demandes', 'Consultez chaque dossier et poursuivez les demandes encore en brouillon.', cards)


def client_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.phone = request.POST.get('phone', profile.phone).strip()
        profile.national_id = request.POST.get('national_id', profile.national_id).strip()
        profile.save(update_fields=['phone','national_id'])
    return render(request, 'profile.html', {'profile': profile})


def client_documents(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        kind = request.POST.get('document_type')
        file = request.FILES.get('file')
        allowed = dict(UploadedDocument.TYPES)
        if kind in allowed and file:
            UploadedDocument.objects.create(profile=profile, document_type=kind, file=file)
    return render(request, 'documents.html', {'profile': profile, 'documents': profile.documents.order_by('-created_at')})


def client_notifications(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    notes = profile.notifications.order_by('-created_at')
    return render(request, 'notifications.html', {'profile': profile, 'notifications': notes})


def client_payments(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    payments = Payment.objects.filter(loan__profile=profile).select_related('loan').order_by('-created_at')
    return render(request, 'list_page.html', {'title':'Historique des paiements','eyebrow':'ESPACE CLIENT','description':'Tous les encaissements enregistrés sur vos prêts.','columns':['Date','Prêt','Montant','Mode','Reçu'],'rows':[[p.created_at.strftime('%d/%m/%Y %H:%M'),str(p.loan.principal),f'{p.amount:,.0f} FC',p.method,p.receipt.number if hasattr(p,'receipt') else '—'] for p in payments]})


def client_receipts(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    receipts = PaymentReceipt.objects.filter(payment__loan__profile=profile).select_related('payment__loan').order_by('-created_at')
    return render(request, 'list_page.html', {'title':'Mes reçus','eyebrow':'ESPACE CLIENT','description':'Références de reçus générées par DEFA.','columns':['Reçu','Date','Montant','Prêt'],'rows':[[r.number,r.created_at.strftime('%d/%m/%Y %H:%M'),f'{r.payment.amount:,.0f} FC',f'{r.payment.loan.principal:,.0f} FC'] for r in receipts]})


def client_schedule(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    installments = Installment.objects.filter(loan__profile=profile).select_related('loan').order_by('due_date')
    return render(request, 'list_page.html', {'title':'Échéancier','eyebrow':'ESPACE CLIENT','description':'Échéances et paiements appliqués automatiquement.','columns':['Prêt','#','Échéance','À payer','Payé','Statut'],'rows':[[f'{i.loan.principal:,.0f} FC',i.number,i.due_date.strftime('%d/%m/%Y'),f'{i.amount_due:,.0f} FC',f'{i.amount_paid:,.0f} FC',i.get_status_display()] for i in installments]})


def client_payment_detail(request, pk):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    payment = Payment.objects.get(pk=pk, loan__profile=profile)
    receipt = getattr(payment, 'receipt', None)
    return render(request, 'portal_page.html', {'page_title':'Détail du paiement','eyebrow':'PAIEMENT','page_description':'Transaction enregistrée et traçable.','cards':[{'title':'Montant','value':f'{payment.amount:,.0f} FC','text':f'Mode : {payment.method}'},{'title':'Date','value':payment.created_at.strftime('%d/%m/%Y %H:%M'),'text':f'Reçu : {receipt.number if receipt else "—"}'},{'title':'Prêt','value':f'{payment.loan.principal:,.0f} FC','text':payment.loan.status}]})


def client_receipt_detail(request, number):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    receipt = PaymentReceipt.objects.get(number=number, payment__loan__profile=profile)
    return render(request, 'portal_page.html', {'page_title':'Reçu DEFA','eyebrow':'REÇU','page_description':'Document de preuve de paiement.','cards':[{'title':'Numéro','value':receipt.number,'text':'Référence unique'},{'title':'Montant','value':f'{receipt.payment.amount:,.0f} FC','text':receipt.payment.created_at.strftime('%d/%m/%Y %H:%M')},{'title':'Prêt','value':f'{receipt.payment.loan.principal:,.0f} FC','text':'Transaction confirmée'}]})


def client_loan_contract(request, pk):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    loan = Loan.objects.get(pk=pk, profile=profile)
    contract = getattr(loan, 'contract', None)
    return render(request, 'portal_page.html', {'page_title':'Contrat de prêt','eyebrow':'CONTRAT','page_description':'Conditions enregistrées pour ce prêt.','cards':[{'title':'Capital','value':f'{loan.principal:,.0f} FC','text':'Montant initial'},{'title':'Total dû','value':f'{loan.total_due:,.0f} FC','text':f'Statut contrat : {contract.get_status_display() if contract else "Non créé"}'},{'title':'Conditions','value':f'{contract.terms if contract else "—"}','text':'Conservez ce document pour vos archives.'}]})


def agent_clients(request):
    profile = Profile.objects.get(user=request.user)
    assignments = AgentAssignment.objects.filter(agent=profile).select_related('application__profile__user')
    rows = [[a.application.profile.user.get_full_name() or a.application.profile.user.username, f'{a.application.amount:,.0f} FC', a.get_status_display()] for a in assignments]
    return render(request, 'list_page.html', {'title':'Clients assignés','eyebrow':'ESPACE AGENT','description':'Portefeuille confié à votre compte.','columns':['Client','Montant','Affectation'],'rows':rows})


def agent_visits(request):
    profile = Profile.objects.get(user=request.user)
    visits = VerificationVisit.objects.filter(agent=profile).order_by('-scheduled_at')
    rows = [[v.application.profile.user.get_full_name() or v.application.profile.user.username, v.scheduled_at.strftime('%d/%m/%Y %H:%M') if v.scheduled_at else '—', v.get_result_display()] for v in visits]
    return render(request, 'list_page.html', {'title':'Visites terrain','eyebrow':'ESPACE AGENT','description':'Visites de vérification autorisées et traçables.','columns':['Client','Planifiée','Résultat'],'rows':rows})


def agent_payments(request):
    profile = Profile.objects.get(user=request.user)
    payments = Payment.objects.filter(agent=profile).order_by('-created_at')
    rows = [[p.created_at.strftime('%d/%m/%Y %H:%M'),f'{p.amount:,.0f} FC',p.method,p.loan.status] for p in payments]
    return render(request, 'list_page.html', {'title':'Paiements enregistrés','eyebrow':'ESPACE AGENT','description':'Encaissements associés à votre compte.','columns':['Date','Montant','Mode','Prêt'],'rows':rows})


def agent_collection(request):
    profile = Profile.objects.get(user=request.user)
    visits = CollectionVisit.objects.filter(agent=profile).select_related('loan__profile__user').order_by('-scheduled_at')
    rows = [[v.loan.profile.user.get_full_name() or v.loan.profile.user.username,f'{v.loan.total_due:,.0f} FC',v.get_result_display()] for v in visits]
    return render(request, 'list_page.html', {'title':'Recouvrement','eyebrow':'ESPACE AGENT','description':'Suivi responsable des prêts nécessitant une action.','columns':['Client','Total dû','Résultat'],'rows':rows})


def agent_qr(request):
    return staff_page(request,'Scanner QR','Le scan doit authentifier l’agent et ne révéler que les informations nécessaires à la mission.',[{'title':'QR sécurisé','value':'Prêt actif','text':'Utilisez la route API QR pour valider un dossier.'}],role='AGENT')


def admin_page(request, title, description, cards=None):
    return staff_page(request,title,description,cards,role='ADMIN')


def admin_requests(request):
    apps=LoanApplication.objects.select_related('profile__user').order_by('-created_at')[:100]
    rows=[[a.profile.user.get_full_name() or a.profile.user.username,f'{a.amount:,.0f} FC',f'{a.score}/100',a.get_status_display()] for a in apps]
    return render(request,'list_page.html',{'title':'Demandes de prêt','eyebrow':'ADMINISTRATION','description':'Analyse et décisions des dossiers.','columns':['Client','Montant','Score','Statut'],'rows':rows})


def admin_clients(request):
    profiles=Profile.objects.select_related('user').order_by('-created_at')[:100]
    rows=[[p.user.get_full_name() or p.user.username,p.role,'Vérifié' if p.verified else 'En attente',p.phone] for p in profiles]
    return render(request,'list_page.html',{'title':'Clients','eyebrow':'ADMINISTRATION','description':'Vue portefeuille et statut KYC.','columns':['Client','Rôle','KYC','Téléphone'],'rows':rows})


def admin_loans(request):
    loans=Loan.objects.select_related('profile__user').order_by('-created_at')[:100]
    rows=[[l.profile.user.get_full_name() or l.profile.user.username,f'{l.principal:,.0f} FC',f'{l.total_due:,.0f} FC',l.get_status_display()] for l in loans]
    return render(request,'list_page.html',{'title':'Prêts','eyebrow':'ADMINISTRATION','description':'Portefeuille de prêts et soldes.','columns':['Client','Capital','Total dû','Statut'],'rows':rows})


def admin_payments(request):
    payments=Payment.objects.select_related('loan__profile__user').order_by('-created_at')[:100]
    rows=[[p.created_at.strftime('%d/%m/%Y %H:%M'),p.loan.profile.user.get_full_name() or p.loan.profile.user.username,f'{p.amount:,.0f} FC',p.method] for p in payments]
    return render(request,'list_page.html',{'title':'Paiements','eyebrow':'ADMINISTRATION','description':'Transactions financières récentes.','columns':['Date','Client','Montant','Mode'],'rows':rows})


def admin_documents(request):
    docs=UploadedDocument.objects.select_related('profile__user').order_by('-created_at')[:100]
    rows=[[d.profile.user.get_full_name() or d.profile.user.username,d.get_document_type_display(),d.get_status_display(),d.created_at.strftime('%d/%m/%Y')] for d in docs]
    return render(request,'list_page.html',{'title':'Documents / KYC','eyebrow':'ADMINISTRATION','description':'Documents à vérifier avec accès contrôlé.','columns':['Client','Type','Statut','Date'],'rows':rows})


def admin_alerts(request):
    alerts=FraudAlert.objects.select_related('profile__user').order_by('-created_at')[:100]
    rows=[[a.profile.user.get_full_name() or a.profile.user.username,a.rule,a.get_severity_display(),a.get_status_display()] for a in alerts]
    return render(request,'list_page.html',{'title':'Alertes fraude','eyebrow':'ADMINISTRATION','description':'Signaux nécessitant une analyse humaine.','columns':['Client','Règle','Sévérité','Statut'],'rows':rows})


def admin_audit(request):
    logs=AuditLog.objects.select_related('actor__user').order_by('-created_at')[:100]
    rows=[[l.created_at.strftime('%d/%m/%Y %H:%M'),l.actor.user.username if l.actor else 'Système',l.action,l.object_type] for l in logs]
    return render(request,'list_page.html',{'title':'Journal d’audit','eyebrow':'ADMINISTRATION','description':'Historique des opérations sensibles.','columns':['Date','Acteur','Action','Objet'],'rows':rows})


def admin_settings(request):
    settings=SystemSetting.objects.order_by('key')
    rows=[[s.key,str(s.value),s.description] for s in settings]
    return render(request,'list_page.html',{'title':'Paramètres DEFA','eyebrow':'ADMINISTRATION','description':'Paramètres configurables du système.','columns':['Clé','Valeur','Description'],'rows':rows})


def dashboard_kpis(request):
    apps=LoanApplication.objects.count(); loans=Loan.objects.count(); paid=Payment.objects.aggregate(v=Sum('amount'))['v'] or 0
    active=Loan.objects.filter(status='ACTIVE').count(); late=Loan.objects.filter(status='LATE').count(); alerts=FraudAlert.objects.filter(status='OPEN').count()
    return admin_page(request,'Dashboard général','Vue synthétique du portefeuille DEFA.',[{'title':'Demandes','value':apps,'text':'Dossiers'},{'title':'Prêts actifs','value':active,'text':f'{loans} prêts au total'},{'title':'Remboursements','value':f'{paid:,.0f} FC','text':'Total enregistré'},{'title':'Retards','value':late,'text':'Prêts en retard'},{'title':'Alertes','value':alerts,'text':'Alertes ouvertes'}])


def page(request, title, description, area='public', eyebrow=None):
    if area == 'client':
        return client_page(request,title,description)
    if area == 'agent':
        return staff_page(request,title,description,role='AGENT')
    if area == 'admin':
        return admin_page(request,title,description)
    return public_page(request,title,eyebrow or 'DEFA',description)
