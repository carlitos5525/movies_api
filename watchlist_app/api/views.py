from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view()
def movie_list(request):
    movies = Movie.objects.all()
    print(movies)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view()
def movie_detail(request, pk):
    movie = Movie.objects.get(id=pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
