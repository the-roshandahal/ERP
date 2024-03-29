# Generated by Django 3.2 on 2023-07-06 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(max_length=255)),
                ('product_description', models.TextField(blank=True, null=True)),
                ('is_vatable', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': '01. Products',
            },
        ),
        migrations.CreateModel(
            name='ProductBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_batch', models.CharField(blank=True, max_length=255, null=True)),
                ('product_quantity', models.IntegerField(blank=True, null=True)),
                ('product_price', models.FloatField()),
                ('purchase_price', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'verbose_name_plural': '01. Product Batch',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_category', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': '02. Products Category',
            },
        ),
        migrations.CreateModel(
            name='ProductUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_unit', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': '03. Products Unit',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_title', models.CharField(max_length=255)),
                ('service_price', models.FloatField()),
                ('service_description', models.TextField(blank=True, null=True)),
                ('is_vatable', models.BooleanField(default=True)),
                ('service_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productcategory')),
                ('service_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productunit')),
            ],
            options={
                'verbose_name_plural': '01. Services',
            },
        ),
        migrations.CreateModel(
            name='ProductStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('created_by', models.CharField(max_length=255)),
                ('remarks', models.TextField()),
                ('quantity', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productbatch')),
            ],
            options={
                'verbose_name_plural': '10. Product Statement',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productunit'),
        ),
    ]
