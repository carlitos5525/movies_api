from django.urls import path, include
# from watchlist_app.api import views
from watchlist_app.api import views


urlpatterns = [
    path('list/', views.WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', views.WacthDetailAV.as_view(), name='movie-detail'),
    path('stream/', views.StreamPlatformListAV.as_view(), name='stream-list'),
    path('stream/<int:pk>/', views.StreamPlatformDetailAV.as_view(), name='stream-detail'),
]
