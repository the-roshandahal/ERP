# Generated by Django 3.2 on 2023-03-02 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction', models.CharField(max_length=255)),
                ('details', models.CharField(max_length=255)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('payment', models.FloatField(blank=True, null=True)),
                ('balance', models.FloatField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
            options={
                'verbose_name_plural': '05. Statements',
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('bank_transfer', 'bank_transfer'), ('esewa', 'esewa'), ('cash', 'cash')], max_length=255)),
                ('paid_amount', models.FloatField()),
                ('payment_receipt', models.FileField(blank=True, null=True, upload_to='receipts')),
                ('remarks', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
            options={
                'verbose_name_plural': '04. Receipts',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('misc_name', models.CharField(blank=True, max_length=255, null=True)),
                ('misc_amount', models.FloatField(blank=True, null=True)),
                ('deduction_name', models.CharField(blank=True, max_length=100, null=True)),
                ('deduction_amount', models.FloatField(blank=True, null=True)),
                ('discount', models.FloatField(blank=True, null=True)),
                ('vat_amount', models.FloatField(blank=True, null=True)),
                ('sub_total', models.FloatField()),
                ('vatable_amount', models.FloatField()),
                ('total', models.FloatField()),
                ('previous_due', models.FloatField(blank=True, null=True)),
                ('grand_total', models.FloatField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.package')),
            ],
            options={
                'verbose_name_plural': '03. Invoices',
            },
        ),
    ]