# Generated by Django 3.2 on 2023-03-10 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0004_alter_logsheet_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logsheet',
            name='punch_out_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='logsheet',
            name='tasks',
            field=models.TextField(blank=True, null=True),
        ),
    ]
