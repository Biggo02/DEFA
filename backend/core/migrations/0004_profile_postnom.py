from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0003_alter_auditlog_options_alter_installment_options')]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='postnom',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
