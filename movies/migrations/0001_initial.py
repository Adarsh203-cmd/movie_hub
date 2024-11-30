# Generated by Django 5.1.3 on 2024-11-28 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(max_length=100, unique=True, verbose_name='Genre Name')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='Full Name')),
                ('role_type', models.CharField(choices=[('Actor', 'Actor'), ('Director', 'Director'), ('Technician', 'Technician')], max_length=50, verbose_name='Role Type')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_title', models.CharField(max_length=200, verbose_name='Movie Title')),
                ('release_year', models.PositiveIntegerField(verbose_name='Release Year')),
                ('average_user_rating', models.FloatField(verbose_name='Average User Rating')),
                ('genres', models.ManyToManyField(related_name='movies', to='movies.genre', verbose_name='Genres')),
                ('associated_people', models.ManyToManyField(related_name='movies', to='movies.person', verbose_name='Associated People')),
            ],
        ),
    ]