# Generated by Django 4.0.3 on 2023-10-26 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0033_employeedetails_document_base64_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='document_base64',
            field=models.TextField(blank=True, null=True),
        ),
    ]
