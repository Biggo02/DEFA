# Generated initial schema for DEFA.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import uuid
from decimal import Decimal

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Profile', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('role', models.CharField(choices=[('CLIENT','Client'),('AGENT','Agent'),('ANALYST','Analyste'),('ADMIN','Administrateur')], default='CLIENT', max_length=20)),
            ('phone', models.CharField(blank=True, max_length=30)), ('national_id', models.CharField(blank=True, max_length=100)),
            ('photo', models.ImageField(blank=True, null=True, upload_to='profiles/')), ('verified', models.BooleanField(default=False)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),]),
        migrations.CreateModel(name='Address', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('kind', models.CharField(choices=[('HOME','Domicile'),('BUSINESS','Commerce')], max_length=20)), ('address', models.TextField()),
            ('city', models.CharField(max_length=100)), ('neighborhood', models.CharField(blank=True,max_length=100)),
            ('latitude', models.DecimalField(blank=True,decimal_places=6,max_digits=9,null=True)), ('longitude', models.DecimalField(blank=True,decimal_places=6,max_digits=9,null=True)),
            ('verified', models.BooleanField(default=False)), ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='addresses',to='core.profile'))]),
        migrations.CreateModel(name='Employment', fields=[
            ('id', models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')), ('status',models.CharField(default='EMPLOYED',max_length=40)),
            ('employer',models.CharField(blank=True,max_length=200)), ('position',models.CharField(blank=True,max_length=150)),
            ('monthly_income',models.DecimalField(decimal_places=2,default=0,max_digits=14)), ('years_active',models.DecimalField(decimal_places=2,default=0,max_digits=5)),
            ('verified',models.BooleanField(default=False)), ('profile',models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,related_name='employment',to='core.profile'))]),
        migrations.CreateModel(name='Business', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')), ('name',models.CharField(max_length=200)), ('activity',models.CharField(max_length=200)),
            ('years_active',models.DecimalField(decimal_places=2,default=0,max_digits=5)), ('monthly_revenue',models.DecimalField(decimal_places=2,default=0,max_digits=14)),
            ('monthly_expenses',models.DecimalField(decimal_places=2,default=0,max_digits=14)), ('verified',models.BooleanField(default=False)),
            ('profile',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='businesses',to='core.profile'))]),
        migrations.CreateModel(name='Reference', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')), ('name',models.CharField(max_length=150)), ('relationship',models.CharField(max_length=100)), ('phone',models.CharField(max_length=30)), ('verified',models.BooleanField(default=False)),
            ('profile',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='references',to='core.profile'))]),
        migrations.CreateModel(name='LoanApplication', fields=[
            ('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),
            ('amount',models.DecimalField(decimal_places=2,max_digits=14,validators=[django.core.validators.MinValueValidator(Decimal('1'))])), ('duration_days',models.PositiveIntegerField(default=30)), ('frequency',models.CharField(default='WEEKLY',max_length=20)),
            ('purpose',models.CharField(choices=[('BUSINESS','Commerce'),('STOCK','Stock'),('EQUIPMENT','Équipement'),('PERSONAL','Personnel'),('EMERGENCY','Urgence'),('OTHER','Autre')],max_length=30)), ('purpose_detail',models.TextField(blank=True)),
            ('monthly_income',models.DecimalField(decimal_places=2,default=0,max_digits=14)), ('monthly_expenses',models.DecimalField(decimal_places=2,default=0,max_digits=14)), ('score',models.PositiveSmallIntegerField(default=0,validators=[django.core.validators.MaxValueValidator(100)])), ('risk_class',models.CharField(default='D',max_length=1)),
            ('status',models.CharField(choices=[('DRAFT','Brouillon'),('SUBMITTED','Soumise'),('VERIFYING','En vérification'),('REVIEW','Analyse'),('MORE_INFO','Informations complémentaires'),('APPROVED','Approuvée'),('REJECTED','Refusée')],default='DRAFT',max_length=20)), ('submitted_at',models.DateTimeField(blank=True,null=True)), ('created_at',models.DateTimeField(auto_now_add=True)), ('updated_at',models.DateTimeField(auto_now=True)),
            ('profile',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='applications',to='core.profile'))]),
        migrations.CreateModel(name='VerificationVisit', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')), ('scheduled_at',models.DateTimeField(blank=True,null=True)), ('visited_at',models.DateTimeField(blank=True,null=True)),
            ('result',models.CharField(choices=[('PENDING','En attente'),('VERIFIED','Vérifié'),('REVIEW','À revoir'),('FAILED','Impossible')],default='PENDING',max_length=20)), ('notes',models.TextField(blank=True)),
            ('latitude',models.DecimalField(blank=True,decimal_places=6,max_digits=9,null=True)), ('longitude',models.DecimalField(blank=True,decimal_places=6,max_digits=9,null=True)),
            ('agent',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='visits',to='core.profile')), ('application',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='visits',to='core.loanapplication'))]),
        migrations.CreateModel(name='Loan', fields=[
            ('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)), ('principal',models.DecimalField(decimal_places=2,max_digits=14)), ('total_due',models.DecimalField(decimal_places=2,max_digits=14)), ('disbursed_at',models.DateTimeField(blank=True,null=True)),
            ('status',models.CharField(choices=[('ACTIVE','Actif'),('LATE','En retard'),('PAID','Remboursé'),('CANCELLED','Annulé')],default='ACTIVE',max_length=20)), ('qr_token',models.UUIDField(default=uuid.uuid4,editable=False,unique=True)), ('created_at',models.DateTimeField(auto_now_add=True)),
            ('application',models.OneToOneField(on_delete=django.db.models.deletion.PROTECT,related_name='loan',to='core.loanapplication')), ('profile',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='loans',to='core.profile'))]),
        migrations.CreateModel(name='Installment', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')), ('number',models.PositiveIntegerField()), ('due_date',models.DateField()), ('amount_due',models.DecimalField(decimal_places=2,max_digits=14)), ('amount_paid',models.DecimalField(decimal_places=2,default=0,max_digits=14)),
            ('status',models.CharField(choices=[('UPCOMING','À venir'),('DUE','À payer'),('PARTIAL','Partielle'),('PAID','Payée'),('LATE','En retard')],default='UPCOMING',max_length=20)), ('loan',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='installments',to='core.loan'))]),
        migrations.CreateModel(name='Payment', fields=[
            ('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)), ('amount',models.DecimalField(decimal_places=2,max_digits=14,validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])), ('method',models.CharField(default='CASH',max_length=30)), ('client_confirmed',models.BooleanField(default=False)), ('created_at',models.DateTimeField(auto_now_add=True)),
            ('agent',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.PROTECT,related_name='payments_collected',to='core.profile')), ('installment',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.PROTECT,related_name='payments',to='core.installment')), ('loan',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='payments',to='core.loan'))]),
        migrations.CreateModel(name='PaymentReceipt', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')), ('number',models.CharField(max_length=40,unique=True)), ('created_at',models.DateTimeField(auto_now_add=True)), ('payment',models.OneToOneField(on_delete=django.db.models.deletion.PROTECT,related_name='receipt',to='core.payment'))]),
        migrations.CreateModel(name='Consent', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')), ('kind',models.CharField(max_length=60)), ('granted',models.BooleanField(default=False)), ('granted_at',models.DateTimeField(blank=True,null=True)), ('version',models.CharField(default='1.0',max_length=20)), ('profile',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='consents',to='core.profile'))]),
        migrations.CreateModel(name='AuditLog', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')), ('action',models.CharField(max_length=120)), ('object_type',models.CharField(blank=True,max_length=80)), ('object_id',models.CharField(blank=True,max_length=100)), ('metadata',models.JSONField(blank=True,default=dict)), ('created_at',models.DateTimeField(auto_now_add=True)), ('actor',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.PROTECT,to='core.profile'))]),
        migrations.AlterUniqueTogether(name='installment',unique_together={('loan','number')}),
    ]
