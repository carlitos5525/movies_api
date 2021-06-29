from rest_framework.views import APIView
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import StreamPlataformSerializer, WatchListSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics


# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(id=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie not found'} ,status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         try:
#             movie = Movie.objects.get(id=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie not found'} ,status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(instance=movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         try:
#             movie = Movie.objects.get(id=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie not found'} ,status=status.HTTP_404_NOT_FOUND)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class WacthDetailAV(APIView):

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(instance=movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformListAV(APIView):

    def get(self, request):
        stream_platforms = StreamPlatform.objects.all()
        serializer = StreamPlataformSerializer(stream_platforms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlataformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):

    def get(self, request, pk):
        try:
            stream_platform = StreamPlatform.objects.get(id=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Stream platform does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlataformSerializer(stream_platform)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            stream_platform = StreamPlatform.get(id=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Stream platform does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlataformSerializer(data=request.data, instance=stream_platform)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        try:
            stream_platform = StreamPlatform.objects.get(id=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Stream platform does not exist'}, status=status.HTTP_404_NOT_FOUND)
        stream_platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer    
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer 

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)   

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(id=pk)

        serializer.save(watchlist=watchlist)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
