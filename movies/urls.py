from django.urls import path
from .views import MovieListCreateView, MovieDetailView, ActorDeleteView

urlpatterns = [
    path('movies/', MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('actors/<int:pk>/delete/', ActorDeleteView.as_view(), name='actor-delete'),
]
