""" from django.shortcuts import render
from watchlist_app.models import Movie
from django.http import JsonResponse
# Create your views here.JsonResponse

def movie_list(request):
    movies=Movie.objects.all().values()
    data={'movies' : list(movies)}
    return JsonResponse(data)


def movie_details(request,pk):
    movie=Movie.objects.get(pk =pk)
    data={'name' : movie.name, 'description' : movie.description}
    print(movie)
    return JsonResponse(data)
 """