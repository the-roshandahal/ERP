# Generated by Django 3.2 on 2023-03-09 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rename_manage_lead_permission_manage_leads'),
        ('features', '0003_auto_20230309_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logsheet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.companyuser'),
        ),
    ]
