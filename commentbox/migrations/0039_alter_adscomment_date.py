# Generated by Django 5.0 on 2024-01-02 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commentbox', '0038_alter_adscomment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adscomment',
            name='date',
            field=models.CharField(default='2024-01-02', max_length=10),
        ),
    ]
