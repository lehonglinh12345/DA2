# Generated by Django 5.1 on 2025-03-20 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_movie_video_movie_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
