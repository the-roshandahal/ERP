# Generated by Django 3.2 on 2023-03-09 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rename_manage_lead_permission_manage_leads'),
        ('features', '0002_auto_20230309_1227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='task_to',
        ),
        migrations.AddField(
            model_name='todo',
            name='task_to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.companyuser'),
            preserve_default=False,
        ),
    ]