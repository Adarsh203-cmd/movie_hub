# Generated by Django 5.1.3 on 2024-11-29 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_average_user_rating_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['movie_title'], name='movie_title_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['release_year'], name='release_year_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['average_user_rating'], name='avg_rating_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['full_name'], name='full_name_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['role_type'], name='role_type_idx'),
        ),
    ]
