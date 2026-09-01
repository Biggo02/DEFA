from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_risk_compliance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auditlog',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='installment',
            options={'ordering': ['number']},
        ),
    ]
