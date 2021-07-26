from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    email = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.email)


class Channel(models.Model):
    name = models.CharField(max_length=255)
    banner = models.ImageField(max_length=255)
    profile_pic = models.ImageField(blank=True, null=True, default=None)
    description = models.TextField()
    subscribers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ',' + str(self.name)


class Video(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    name = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(blank=True, null=True, default=None)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ',' + str(self.name)


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    commenter_name = models.CharField(max_length=255, default="")
    commenter_image = models.ImageField(blank=True, null=True, default=None)
    comment = models.CharField(max_length=255, default="")
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
