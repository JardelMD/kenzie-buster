from django.shortcuts import get_object_or_404
from movies.models import Movie
from movies_orders.serializers import MovieOrderSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class MovieOrderView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, movie_id: int) -> Response:
        found_movie = get_object_or_404(Movie.objects.all(), pk=movie_id)
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, movie=found_movie)
        return Response(serializer.data, status.HTTP_201_CREATED)
