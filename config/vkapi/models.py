from django.db import models


class Profile(models.Model):
    profile_id = models.CharField(max_length=255)
    avatar_url = models.URLField()
    followers = models.PositiveIntegerField()
    following = models.PositiveIntegerField()


class Post(models.Model):
    post_id = models.CharField(max_length=255)
    url = models.URLField()
    likes = models.PositiveIntegerField()
    share = models.PositiveIntegerField()
    views = models.PositiveIntegerField()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # Add other fields as needed
