# Generated by Django 4.1.4 on 2023-03-04 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_permission_create_hrm_permission_create_service_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='permission',
            old_name='create_service',
            new_name='create_products',
        ),
        migrations.RenameField(
            model_name='permission',
            old_name='delete_service',
            new_name='delete_products',
        ),
        migrations.RenameField(
            model_name='permission',
            old_name='read_service',
            new_name='read_products',
        ),
        migrations.RenameField(
            model_name='permission',
            old_name='update_service',
            new_name='update_products',
        ),
    ]