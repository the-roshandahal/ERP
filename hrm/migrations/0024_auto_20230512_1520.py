# Generated by Django 3.2 on 2023-05-12 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0023_alter_devicedata_port'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceattendance',
            name='punchin_timestamp',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='deviceattendance',
            name='punchout_timestamp',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
