from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Genre(models.Model):
    genre_name = models.CharField(max_length=100, unique=True, verbose_name="Genre Name")

    def __str__(self):
        return self.genre_name

class Person(models.Model):
    ROLE_CHOICES = [
        ('Actor', 'Actor'),
        ('Director', 'Director'),
        ('Technician', 'Technician'),
    ]
    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    role_type = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name="Role Type")

    class Meta:
        indexes = [
            models.Index(fields=['full_name'], name='full_name_idx'),
            models.Index(fields=['role_type'], name='role_type_idx'),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.role_type})"

class Movie(models.Model):
    movie_title = models.CharField(max_length=200, verbose_name="Movie Title", db_index = True)
    release_year = models.PositiveIntegerField(verbose_name="Release Year", db_index= True)
    average_user_rating = models.FloatField(verbose_name="Average User Rating", validators=[MinValueValidator(0,0), MaxValueValidator(10,0)])
    genres = models.ManyToManyField(Genre, related_name='movies', verbose_name="Genres")
    associated_people = models.ManyToManyField(Person, related_name='movies', verbose_name="Associated People")

    class Meta:
        indexes = [
            models.Index(fields=['movie_title'], name='movie_title_idx'),
            models.Index(fields=['release_year'], name='release_year_idx'),
            models.Index(fields=['average_user_rating'], name='avg_rating_idx'),
        ]

    def __str__(self):
        return self.movie_title