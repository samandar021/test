from django.db import models


class Profile(models.Model):
    profile_id = models.CharField(max_length=20)
    avatar_url = models.URLField()
    followers = models.CharField(max_length=10)
    following = models.CharField(max_length=10)


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=20)
    url = models.URLField()
    likes = models.CharField(max_length=10)
    share = models.CharField(max_length=10)
    views = models.CharField(max_length=10)
