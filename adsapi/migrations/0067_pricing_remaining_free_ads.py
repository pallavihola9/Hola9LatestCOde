# Generated by Django 5.0 on 2024-01-04 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adsapi', '0066_alter_adsmangeme_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricing',
            name='remaining_free_ads',
            field=models.IntegerField(default=10),
        ),
    ]
