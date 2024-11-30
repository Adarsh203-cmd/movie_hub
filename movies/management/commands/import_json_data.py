import json
from django.core.management.base import BaseCommand
from movies.models import Genre, Person, Movie

class Command(BaseCommand):
    help = 'Import data from a JSON file to populate the database'

    def handle(self, *args, **kwargs):
        # Load JSON data from the file
        with open('data.json', 'r') as file:
            data = json.load(file)

        # Insert Genres
        for genre_data in data.get('genres', []):
            genre, created = Genre.objects.get_or_create(genre_name=genre_data['genre_name'])
            if created:
                self.stdout.write(self.style.SUCCESS(f"Genre '{genre.genre_name}' added"))

        # Insert Persons
        for person_data in data.get('persons', []):
            role_type = person_data.get('role_type', 'Actor')

            #check if role_type s valid
            if role_type not in dict(Person.ROLE_CHOICES):
                self.stdout.write(self.style.ERROR(f"Invalid role type: {role_type} for {person_data['full_name']}"))
                continue  # Skip invalid entries
            try:
                # Check if the person exists in the database
                person = Person.objects.filter(full_name=person_data['full_name'].strip()).first()

                if person:
                    #If person exist but the role_tyoe is incorrect, update it
                    if person.role_type!=role_type:
                        old_role = person.role_type
                        person.role_type=role_type
                        person.save()
                        self.stdout.write(self.style.SUCCESS(
                            f"Updated '{person.full_name}': role_type changed from '{old_role}' to '{person.role_type}'"
                        ))
                    else:
                        self.stdout.write(self.style.WARNING(f"Person '{person.full_name}' already exists with correct role_type '{person.role_type}'"))
                else:
                     #Attempt to get or create the person
                    Person.objects.create(full_name=person_data['full_name'].strip(), role_type=role_type)
                    self.stdout.write(self.style.SUCCESS(f"Person '{person_data['full_name']}' added as {role_type}"))
            except Exception as e:
                #print the error for debugging
                self.stdout.write(self.style.ERROR(f"Error creating person {person_data['full_name']}: {str(e)}"))

        # Insert Movies
        for movie_data in data.get('movies', []):
            movie, created = Movie.objects.get_or_create(
                movie_title=movie_data['movie_title'],
                release_year=movie_data['release_year'],
                average_user_rating=movie_data['average_user_rating']
            )

            # Link genres to the movie
            for genre_name in movie_data.get('genres', []):
                genre, created = Genre.objects.get_or_create(genre_name=genre_name)
                movie.genres.add(genre)

            # Link persons (associated people) to the movie
            for person_name in movie_data.get('associated_people', []):
                # Use get_or_create to ensure the person exists before linking to the movie
                person, created = Person.objects.get_or_create(full_name=person_name)
                movie.associated_people.add(person)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Movie '{movie.movie_title}' added"))
