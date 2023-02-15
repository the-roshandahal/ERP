# Generated by Django 3.2 on 2023-02-15 07:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0006_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='CompanyUser',
        ),
        migrations.AlterModelOptions(
            name='companyuser',
            options={'verbose_name_plural': '03. Company User'},
        ),
    ]
