from django.contrib import admin
from .models import Channel, Video, Comment


# Register your models here.
class ChannelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "banner", "profile_pic", "description", 'subscribers', "created_at", "updated_at"]


class VideoAdmin(admin.ModelAdmin):
    list_display = ["id", "channel", "name", "description", "thumbnail", "likes", "views", "created_at", "updated_at"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "video", "commenter_name","commenter_image", "comment", "likes", "created_at", "updated_at"]


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Comment, CommentAdmin)
