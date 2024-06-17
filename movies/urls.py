from django.urls import path
from movies.views import MovieView
from . import views

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/", views.MovieDetailView.as_view()),
]
