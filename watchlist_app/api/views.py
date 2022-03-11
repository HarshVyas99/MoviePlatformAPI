from watchlist_app.models import WatchList
from watchlist_app.models import StreamPlatform,Review,User
from watchlist_app.api.serializers import WatchListSerializer
from watchlist_app.api.serializers import StreamPlatformSerializer,ReviewSerializer
from watchlist_app.api.permissions import IsAdminorReadOnly,IsReviewUserorReadOnly
from watchlist_app.api.pagination import WatchListPagination
from django.contrib.auth.models import User
#from django.core.exceptions import ValidationError
from rest_framework.serializers import ValidationError 
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from django.shortcuts import get_object_or_404

class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
         return Review.objects.all()
    
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        watchl=WatchList.objects.get(pk=pk)
        
        review_user=self.request.user
        print(review_user)
        review_queryset=Review.objects.filter(watchlist=pk,review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")
        
        if watchl.number_rating == 0:
            watchl.avg_rating = serializer.validated_data['rating']
            watchl.number_of_rating = watchl.number_rating + 1
        else:
            watchl.avg_rating = (watchl.avg_rating * watchl.number_rating + serializer.validated_data['rating'])
            watchl.number_rating = watchl.number_rating + 1
            watchl.avg_rating = watchl.avg_rating / watchl.number_rating
            
        watchl.number_rating=watchl.number_rating+1
        watchl.save()
        print(watchl)
        print(serializer.validated_data)
        serializer.save(watchlist=watchl,review_user=review_user)


class WatchListFilter(generics.ListAPIView):
    #throttle_classes = [UserRateThrottle,AnonRateThrottle]
    #permission_classes = [IsAdminorReadOnly]
    
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']
    pagination_class = WatchListPagination
    # def get_queryset(self):
    #     pk=self.kwargs['pk']
    #     review=Review.objects.filter(watchlist=pk)
    #     return review    

class ReviewListFilter(generics.ListAPIView):
    #throttle_classes = [UserRateThrottle,AnonRateThrottle]
    #permission_classes = [IsAdminorReadOnly]
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    # def get_queryset(self):
    #     pk=self.kwargs['pk']
    #     review=Review.objects.filter(watchlist=pk)
    #     return review         

class ReviewList(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    #permission_classes = [IsAdminorReadOnly]
    
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        pk=self.kwargs['pk']
        review=Review.objects.filter(watchlist=pk)
        return review
        

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    permission_classes = [IsReviewUserorReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetail(mixins.RetrieveModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

class StreamPlatformViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminorReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
# class StreamPlatformViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         Streamplatform = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(Streamplatform)
#         return Response(serializer.data)


class StreamPlatformListAV(APIView):
    permission_classes = [IsAdminorReadOnly]
    def get(self, request, *args, **kwargs):
        StreamPlatformList=StreamPlatform.objects.all()
        serializer=StreamPlatformSerializer(StreamPlatformList,many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer=StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminorReadOnly]
    def get(self, request,pk, *args, **kwargs):
        try:
            Streamplatform=StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=StreamPlatformSerializer(Streamplatform)
        return Response(serializer.data)

    def put(self, request,pk, *args, **kwargs):
        Streamplatform=StreamPlatform.objects.get(pk=pk)
        serializer=StreamPlatformSerializer(Streamplatform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request,pk, *args, **kwargs):
        Streamplatform=StreamPlatform.objects.get(pk=pk)
        Streamplatform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):
    permission_classes = [IsAdminorReadOnly]
    
    def get(self, request, *args, **kwargs):
        Watchlist=WatchList.objects.all()
        serializer=WatchListSerializer(Watchlist,many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class WatchListDetailAV(APIView):
    permission_classes = [IsAdminorReadOnly]
    
    def get(self, request,pk, *args, **kwargs):
        try:
            Watchlist=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=WatchListSerializer(Watchlist)
        return Response(serializer.data)

    def put(self, request,pk, *args, **kwargs):
        Watchlist=WatchList.objects.get(pk=pk)
        serializer=WatchListSerializer(Watchlist,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request,pk, *args, **kwargs):
        Watchlist=WatchList.objects.get(pk=pk)
        Watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies=Movie.objects.all()
#         serializer=MovieSerializer(movies,many=True)
#         return Response(serializer.data)
#     if request.method=='POST':
#         serializer=MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        

# @api_view(['GET', 'PUT','DELETE'])
# def movie_details(request,pk):
#     if request.method == 'GET':
#         try:
#             movie=Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
#         serializer=MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie=Movie.objects.get(pk=pk)
#         serializer=MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     if request.method == 'DELETE':
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)