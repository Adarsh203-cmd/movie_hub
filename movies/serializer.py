from rest_framework import serializers
from .models import Genre, Person, Movie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    associated_people = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), many=True)
    genre_details = GenreSerializer(many=True, read_only=True, source='genres')
    associated_people_details = PersonSerializer(many=True, read_only=True, source='associated_people')

    class Meta:
        model = Movie
        fields = [
            'id',
            'movie_title',
            'release_year',
            'average_user_rating',
            'genres',
            'genre_details',
            'associated_people',
            'associated_people_details'
        ]
