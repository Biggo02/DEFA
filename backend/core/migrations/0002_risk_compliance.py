from django.db import migrations, models
import django.db.models.deletion
import uuid

class Migration(migrations.Migration):
    dependencies = [('core','0001_initial')]
    operations = [
        migrations.CreateModel(
            name='UploadedDocument',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('document_type', models.CharField(choices=[('NATIONAL_ID','Pièce d’identité'),('ADDRESS','Preuve de domicile'),('INCOME','Preuve de revenus'),('BUSINESS','Preuve de commerce'),('CONTRACT','Contrat'),('OTHER','Autre')], max_length=30)),
                ('file', models.FileField(max_length=500, upload_to='documents/%Y/%m/')),
                ('status', models.CharField(choices=[('PENDING','En attente'),('VERIFIED','Vérifié'),('REJECTED','Rejeté')], default='PENDING', max_length=20)),
                ('rejection_reason', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='core.profile')),
                ('verified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='documents_verified', to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='AgentAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ASSIGNED','Assignée'),('IN_PROGRESS','En cours'),('COMPLETED','Terminée'),('CANCELLED','Annulée')], default='ASSIGNED', max_length=20)),
                ('due_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assignments', to='core.profile')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='core.loanapplication')),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assignments_created', to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='LocationConsent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(max_length=100)),
                ('granted', models.BooleanField(default=False)),
                ('version', models.CharField(default='1.0', max_length=20)),
                ('granted_at', models.DateTimeField(blank=True, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_consents', to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='LocationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('HOME','Domicile'),('BUSINESS','Commerce'),('VISIT','Visite')], max_length=20)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('accuracy_m', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('captured_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('consent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='records', to='core.locationconsent')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default='1.0', max_length=20)),
                ('status', models.CharField(choices=[('DRAFT','Brouillon'),('PENDING','En attente'),('SIGNED','Signé'),('CANCELLED','Annulé')], default='DRAFT', max_length=20)),
                ('terms', models.JSONField(blank=True, default=dict)),
                ('signed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('loan', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='contract', to='core.loan')),
            ],
        ),
        migrations.CreateModel(
            name='CollectionVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_at', models.DateTimeField(blank=True, null=True)),
                ('visited_at', models.DateTimeField(blank=True, null=True)),
                ('result', models.CharField(choices=[('PENDING','En attente'),('PAID','Paiement reçu'),('PROMISE','Promesse de paiement'),('ABSENT','Client absent'),('ESCALATE','À escalader')], default='PENDING', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='collection_visits', to='core.profile')),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='collection_visits', to='core.loan')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('kind', models.CharField(default='INFO', max_length=40)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='FraudAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.CharField(max_length=120)),
                ('severity', models.CharField(choices=[('LOW','Faible'),('MEDIUM','Moyenne'),('HIGH','Élevée'),('CRITICAL','Critique')], default='MEDIUM', max_length=20)),
                ('status', models.CharField(choices=[('OPEN','Ouverte'),('REVIEWING','En analyse'),('RESOLVED','Résolue'),('DISMISSED','Écartée')], default='OPEN', max_length=20)),
                ('details', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fraud_alerts', to='core.loanapplication')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fraud_alerts', to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='SystemSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True)),
                ('value', models.JSONField(default=dict)),
                ('description', models.TextField(blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
