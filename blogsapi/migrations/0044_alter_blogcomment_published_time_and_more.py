# Generated by Django 5.0 on 2024-01-05 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsapi', '0043_alter_blogcomment_published_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='published_time',
            field=models.CharField(default='2024-01-05', max_length=232),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='published_time',
            field=models.CharField(default='2024-01-05', max_length=150),
        ),
    ]