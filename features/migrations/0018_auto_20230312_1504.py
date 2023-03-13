# Generated by Django 3.2 on 2023-03-12 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0007_auto_20230312_1441'),
        ('features', '0017_alter_company_company_logo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logsheet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrm.employee'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='task_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrm.employee'),
        ),
    ]