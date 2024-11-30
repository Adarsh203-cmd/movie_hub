from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Movie, Person
from .serializer import MovieSerializer

# Pagination class
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

# GET and POST for Movie
class MovieListCreateView(APIView):
    def get(self, request):
        # Get query parameters for filtering
        actor_name = request.query_params.get('actor', None)
        director_name = request.query_params.get('director', None)
        technician_name = request.query_params.get('technician', None)
        search_query = request.query_params.get('search', None)

        # Start the base queryset for movies
        movies = Movie.objects.all().distinct()

        # Filter by actor if provided
        if actor_name:
            actor = Person.objects.filter(full_name__icontains=actor_name, role_type='Actor')
            movies = movies.filter(associated_people__in=actor)

        # Filter by director if provided
        if director_name:
            director = Person.objects.filter(full_name__icontains=director_name, role_type='Director')
            movies = movies.filter(associated_people__in=director)

        # Filter by technician if provided
        if technician_name:
            technician = Person.objects.filter(full_name__icontains=technician_name, role_type='Technician')
            movies = movies.filter(associated_people__in=technician)

        # Search functionality - search by movie title or description
        if search_query:
            movies = movies.filter(
                Q(movie_title__icontains=search_query) | Q(genres__genre_name__icontains=search_query)
            )

        # Paginate the movies queryset
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(movies, request)
        serializer = MovieSerializer(result_page, many=True)

        # Return the paginated response with next and previous links
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Fetch a single Movie or update it
class MovieDetailView(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            updated_movie = serializer.save()
            genres = request.data.get('genres', [])
            associated_people = request.data.get('associated_people', [])

            updated_movie.genres.set(genres)
            updated_movie.associated_people.set(associated_people)

            updated_movie.save()
            return Response(MovieSerializer(updated_movie).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete an actor if not associated with any movies
class ActorDeleteView(APIView):
    def post(self, request, pk):
        try:
            actor = Person.objects.get(pk=pk, role_type='Actor')
        except Person.DoesNotExist:
            return Response({'error': 'Actor not found'}, status=status.HTTP_404_NOT_FOUND)

        if actor.movies.exists():
            return Response({'error': 'Actor is associated with movies and cannot be deleted'}, status=status.HTTP_400_BAD_REQUEST)

        actor.delete()
        return Response({'message': 'Actor deleted successfully'}, status=status.HTTP_200_OK)
