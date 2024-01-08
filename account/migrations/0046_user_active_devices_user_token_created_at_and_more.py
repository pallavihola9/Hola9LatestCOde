# Generated by Django 5.0 on 2024-01-02 06:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0045_alter_jobapply_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active_devices',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='token_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='token_expiration_time',
            field=models.DurationField(default=datetime.timedelta(seconds=1)),
        ),
        migrations.AddField(
            model_name='user',
            name='token_key',
            field=models.CharField(blank=True, max_length=40, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='CustomToken',
        ),
    ]