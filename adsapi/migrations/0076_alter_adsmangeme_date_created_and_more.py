# Generated by Django 5.0 on 2024-01-12 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adsapi', '0075_alter_userrecentads_ads_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adsmangeme',
            name='date_created',
            field=models.CharField(default='2024-01-12', max_length=20),
        ),
        migrations.AlterField(
            model_name='paymentdetailsvalues',
            name='date',
            field=models.CharField(default='2024-01-12', max_length=10),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='ads_timing',
            field=models.CharField(default='2024-01-12', max_length=30),
        ),
        migrations.AlterField(
            model_name='realestateenquery',
            name='date_created',
            field=models.CharField(default='2024-01-12', max_length=150),
        ),
        migrations.AlterField(
            model_name='reportads',
            name='dates',
            field=models.CharField(default='2024-01-12', max_length=30),
        ),
    ]
