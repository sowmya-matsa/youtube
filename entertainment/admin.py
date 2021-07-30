from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Channel, Video, Comment


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ["id"]


class ChannelAdmin(admin.ModelAdmin):
    list_display = ["id","user", "name", "banner", "profile_pic", "description", 'subscribers', "created_at", "updated_at"]


class VideoAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "channel", "name", "description", "thumbnail", "likes", "views", "created_at", "updated_at"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "video", "commenter_name", "commenter_image", "comment", "likes", "created_at", "updated_at"]


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CustomUser,CustomUserAdmin)