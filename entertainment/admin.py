from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Channel, Video, Comment, Category, Subscriber


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ["id"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class ChannelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "category", "name", "banner", "profile_pic", "description",
                    "created_at", "updated_at"]


class VideoAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "channel", "name", "description", "thumbnail", "likes", "views", "video_link",
                    "created_at", "updated_at"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "video", "commenter_name", "commenter_image", "comment", "likes", "created_at",
                    "updated_at"]


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "channel", "created_at"]


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
