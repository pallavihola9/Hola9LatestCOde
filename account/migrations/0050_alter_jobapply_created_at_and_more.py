# Generated by Django 5.0 on 2024-01-10 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0049_alter_jobapply_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapply',
            name='created_at',
            field=models.CharField(default='2024-01-10', max_length=150),
        ),
        migrations.AlterField(
            model_name='jobsrequired',
            name='created_at',
            field=models.CharField(default='2024-01-10', max_length=150),
        ),
        migrations.AlterField(
            model_name='telemetrydaa',
            name='date',
            field=models.CharField(default='2024-01-10', max_length=10),
        ),
    ]
