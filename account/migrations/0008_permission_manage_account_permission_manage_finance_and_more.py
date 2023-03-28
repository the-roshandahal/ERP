# Generated by Django 4.0.3 on 2023-03-28 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_delete_companyuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='manage_account',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='permission',
            name='manage_finance',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='permission',
            name='manage_hrm',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='permission',
            name='manage_products',
            field=models.BooleanField(default=0),
        ),
    ]
