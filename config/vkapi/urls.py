from django.urls import path
from .views import ProfileView, LikesView, PostsListView

urlpatterns = [
    path('api/v1/profile/', ProfileView.as_view(), name='profile'),
    path('api/v1/likes/', LikesView.as_view(), name='likes'),
    path('api/v1/posts/', PostsListView.as_view(), name='Last 10 posts with one post like and shares'),
    path('profile/', ProfileView.as_view(), name='profile-view'),
    path('likes/', LikesView.as_view(), name='likes-view'),


]
