# Generated by Django 4.0.3 on 2023-04-21 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('paymentapi', '0013_enquiry_alter_order_order_datetele_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_dateTele',
            field=models.CharField(default='2023-04-21', max_length=155),
        ),
        migrations.AlterField(
            model_name='transactiondetails',
            name='ordrDate',
            field=models.CharField(default='2023-04-21', max_length=155),
        ),
        migrations.AlterField(
            model_name='transationidone',
            name='date_created',
            field=models.CharField(default='2023-04-21', max_length=550),
        ),
        migrations.CreateModel(
            name='VerifiedCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentMoney', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
