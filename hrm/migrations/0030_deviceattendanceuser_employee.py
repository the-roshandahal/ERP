# Generated by Django 3.2 on 2023-05-14 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0029_alter_holidays_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceattendanceuser',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hrm.employee'),
        ),
    ]