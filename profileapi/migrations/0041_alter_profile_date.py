# Generated by Django 5.0 on 2024-01-04 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapi', '0040_alter_profile_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.CharField(default='2024-01-04', max_length=10),
        ),
    ]