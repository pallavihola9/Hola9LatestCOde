# Generated by Django 4.0.3 on 2023-08-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapi', '0019_alter_profile_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.CharField(default='2023-08-10', max_length=10),
        ),
    ]
