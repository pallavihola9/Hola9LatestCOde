# Generated by Django 5.0 on 2023-12-29 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagesapi', '0036_alter_contact_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.CharField(default='2023-12-29', max_length=150),
        ),
    ]
