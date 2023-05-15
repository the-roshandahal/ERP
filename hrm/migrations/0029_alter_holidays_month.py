# Generated by Django 3.2 on 2023-05-14 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0028_devicedata_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holidays',
            name='month',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holidays', to='hrm.monthsetup'),
        ),
    ]