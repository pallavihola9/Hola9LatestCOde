# Generated by Django 4.0.3 on 2023-12-15 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsapi', '0039_alter_blogcomment_published_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='video/'),
        ),
        migrations.AddField(
            model_name='blogs',
            name='video_base64',
            field=models.TextField(blank=True, null=True),
        ),
    ]
