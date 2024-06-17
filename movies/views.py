from django.shortcuts import get_object_or_404
from movies.models import Movie
from movies.permissions import IsAdminOrReadOlnly
from movies.serializers import MovieSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrReadOlnly,)

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrReadOlnly,)

    def get(self, request: Response, movie_id) -> Response:
        found_movie = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieSerializer(found_movie)
        return Response(serializer.data)

    def delete(self, request: Request, movie_id: int) -> Response:
        try:
            found_movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response(
                {"message": "Movie not found."},
                status.HTTP_404_NOT_FOUND,
            )
        found_movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
