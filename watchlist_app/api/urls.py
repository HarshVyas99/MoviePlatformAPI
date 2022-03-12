from django.urls import path,include
from watchlist_app.api.views import WatchListAV,WatchListFilter
from watchlist_app.api.views import WatchListDetailAV
from watchlist_app.api.views import StreamPlatformListAV
from watchlist_app.api.views import StreamPlatformDetailAV,ReviewList,ReviewDetail,ReviewCreate,StreamPlatformViewSet,ReviewListFilter
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'stream', StreamPlatformViewSet, basename='streamplatform')


urlpatterns = [
    path('movies/', WatchListAV.as_view(), name='watchlist-list'),
    path('movie-filter/', WatchListFilter.as_view(), name='watchlist-list-filter'),
    path('movie-detail/<int:pk>/',WatchListDetailAV.as_view(),name='watchlist-details'),
    #path('',include(router.urls)),
    # path('streamlist/', StreamPlatformListAV.as_view(), name='StreamPlatform-list'),
    # path('streamlist/<int:pk>', StreamPlatformDetailAV.as_view(), name='StreamPlatform-details'),
    # path('review/',ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>',ReviewDetail.as_view(), name='review-detail'),
    path('movie/<int:pk>/review-create/',ReviewCreate.as_view(), name='review-create'),
    path('movie/<int:pk>/reviews/',ReviewList.as_view(), name='review-list'),
    path('movie/reviews-list/',ReviewListFilter.as_view(), name='review-list-filter'),
    path('review/<int:pk>',ReviewDetail.as_view(), name='review-detail'),
    path('',include(router.urls)),
]
