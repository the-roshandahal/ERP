# Generated by Django 3.2 on 2023-03-08 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_category', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': '01. Products Category',
            },
        ),
        migrations.CreateModel(
            name='ProductUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_unit', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': '01. Products Unit',
            },
        ),
    ]