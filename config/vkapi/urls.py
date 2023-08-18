from django.urls import path
from .views import *

urlpatterns = [
    path('v1/profile/', ProfileView.as_view(), name='profile'),
    path('v1/likes/', LikesView.as_view(), name='likes'),
    path('v1/posts/', PostsListView.as_view(), name='Last 10 posts with one post like and shares'),
    path('profile/', ProfileViewD.as_view(), name='profile-view'),
    path('likes/', LikesViewD.as_view(), name='likes-view'),


]
