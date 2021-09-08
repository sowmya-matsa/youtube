"""youtube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from entertainment.views import channel, video, videos, comment, comments, sign_up, category, categories, newsfeed, \
    category_channels, subscribe, channel_subscribers, user_subscriptions, videos_variations

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/', category),
    path('categories/', categories),
    path('channel/', channel),
    path('category_channels/', category_channels),
    path('subscribe/', subscribe),
    path('channel_subscribers/', channel_subscribers),
    path('user_subscriptions/', user_subscriptions),
    path('video/', video),
    path('videos/', videos),
    path('comment/', comment),
    path('comments/', comments),
    path('newsfeed/', newsfeed),
    path('videos_variations/',videos_variations),
    path('sign_up/', sign_up),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
