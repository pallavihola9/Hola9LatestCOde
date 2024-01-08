# Generated by Django 4.0.3 on 2022-12-23 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_product', models.CharField(max_length=100)),
                ('order_amount', models.CharField(max_length=25)),
                ('order_payment_id', models.CharField(max_length=100)),
                ('isPaid', models.BooleanField(default=False)),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('user_email', models.CharField(default='null', max_length=150)),
                ('product_name', models.CharField(default='null', max_length=1530)),
                ('order_dateTele', models.CharField(default='2022-12-23', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='TransationIdone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id1', models.CharField(max_length=2322)),
                ('dateid', models.CharField(max_length=232)),
                ('message', models.CharField(max_length=232)),
                ('ProductData', models.CharField(max_length=43343333, null=True)),
                ('date_created', models.CharField(default='2022-12-23', max_length=50)),
                ('userid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
