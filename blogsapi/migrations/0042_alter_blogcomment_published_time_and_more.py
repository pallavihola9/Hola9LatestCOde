# Generated by Django 5.0 on 2024-01-02 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsapi', '0041_alter_blogcomment_published_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='published_time',
            field=models.CharField(default='2024-01-02', max_length=232),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='published_time',
            field=models.CharField(default='2024-01-02', max_length=150),
        ),
    ]
