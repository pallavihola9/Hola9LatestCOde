# Generated by Django 5.0 on 2024-01-02 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagesapi', '0037_alter_contact_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.CharField(default='2024-01-02', max_length=150),
        ),
    ]
