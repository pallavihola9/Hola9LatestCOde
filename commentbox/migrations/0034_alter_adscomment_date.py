# Generated by Django 4.0.3 on 2023-10-26 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commentbox', '0033_alter_adscomment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adscomment',
            name='date',
            field=models.CharField(default='2023-10-26', max_length=10),
        ),
    ]