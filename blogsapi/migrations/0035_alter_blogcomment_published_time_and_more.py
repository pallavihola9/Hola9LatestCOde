# Generated by Django 4.0.3 on 2023-10-26 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsapi', '0034_alter_blogcomment_published_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='published_time',
            field=models.CharField(default='2023-10-26', max_length=232),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='published_time',
            field=models.CharField(default='2023-10-26', max_length=150),
        ),
    ]
