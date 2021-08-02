from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Channel, Video, Comment, Category


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ["id"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class ChannelAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "category", "name", "banner", "profile_pic", "description", 'subscribers',
                    "created_at", "updated_at"]


class VideoAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "channel", "name", "description", "thumbnail", "likes", "views", "created_at",
                    "updated_at"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "video", "commenter_name", "commenter_image", "comment", "likes", "created_at",
                    "updated_at"]


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
