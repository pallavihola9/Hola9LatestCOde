# Generated by Django 5.0 on 2023-12-29 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapi', '0038_alter_profile_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.CharField(default='2023-12-29', max_length=10),
        ),
    ]
