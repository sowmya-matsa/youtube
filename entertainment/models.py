from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.id)


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return str(self.id) + ',' + str(self.name)


class Channel(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    name = models.CharField(max_length=255)
    banner = models.ImageField(max_length=255)
    profile_pic = models.ImageField(blank=True, null=True, default=None)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ',' + str(self.name)


class Video(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    name = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(blank=True, null=True, default=None)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    video_link = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ',' + str(self.name)


class Comment(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    commenter_name = models.CharField(max_length=255, default="")
    commenter_image = models.ImageField(blank=True, null=True, default=None)
    comment = models.CharField(max_length=255, default="")
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscriber(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
