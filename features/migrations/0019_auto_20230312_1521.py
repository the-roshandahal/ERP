# Generated by Django 3.2 on 2023-03-12 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0018_auto_20230312_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='deadline',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='todo',
            name='priority',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.CharField(default='incomplete', max_length=255),
        ),
        migrations.AlterField(
            model_name='todo',
            name='task_from',
            field=models.CharField(max_length=255),
        ),
    ]