# Generated by Django 4.0.3 on 2023-11-08 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0037_loginprofile_image_base64'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapply',
            name='created_at',
            field=models.CharField(default='2023-11-08', max_length=150),
        ),
        migrations.AlterField(
            model_name='jobsrequired',
            name='created_at',
            field=models.CharField(default='2023-11-08', max_length=150),
        ),
        migrations.AlterField(
            model_name='telemetrydaa',
            name='date',
            field=models.CharField(default='2023-11-08', max_length=10),
        ),
    ]
