# Generated by Django 5.0 on 2024-01-05 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagesapi', '0039_alter_contact_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.CharField(default='2024-01-05', max_length=150),
        ),
    ]
