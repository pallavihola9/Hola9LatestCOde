# Generated by Django 5.0 on 2024-01-05 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commentbox', '0040_alter_adscomment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adscomment',
            name='date',
            field=models.CharField(default='2024-01-05', max_length=10),
        ),
    ]
