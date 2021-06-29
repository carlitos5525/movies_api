from django.urls import path, include
# from watchlist_app.api import views
from watchlist_app.api import views


urlpatterns = [
    path('list/', views.WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', views.WacthDetailAV.as_view(), name='movie-detail'),
    path('stream/', views.StreamPlatformListAV.as_view(), name='stream-list'),
    path('stream/<int:pk>/', views.StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    
    path('stream/<int:pk>/review', views.ReviewList.as_view(), name='review-list'),
    path('stream/<int:pk>/review-create', views.ReviewCreate.as_view(), name='review-create'),
    path('stream/review/<int:pk>', views.ReviewDetail.as_view(), name='review-detail'),
]
