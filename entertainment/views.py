from django.shortcuts import render
from .models import Channel, Video
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError


# Create your views here.
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def channel(request):
    # with this method, we can get the single channel
    if request.method == 'GET':
        channel_id = request.GET.get('channel_id', None)
        if channel_id is None:
            content = {
                'message': 'channel_id is missing'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            channel_info = Channel.objects.get(id=channel_id)
            if channel_info.banner:
                banner_url = channel_info.banner.url
            else:
                banner_url = None
            if channel_info.profile_pic:
                image_url = channel_info.profile_pic.url
            else:
                image_url = None
            content = {
                'name': channel_info.name,
                'banner': banner_url,
                'profile_pic': image_url,
                'description': channel_info.description,
                'subscribers': channel_info.subscribers,
                'created_at': channel_info.created_at,
                'updated_at': channel_info.updated_at,

            }
            return Response(content, status=status.HTTP_200_OK)
        except Channel.DoesNotExist:
            content = {
                'message': 'channel_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            content = {
                'message': 'channel_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        # with this method, we can add new channel
        name = request.POST.get('name', None)
        banner = request.FILES.get('banner', None)
        profile_pic = request.FILES.get('profile_pic', None)
        description = request.POST.get("description", None)
        subscribers = request.POST.get("subscribers", None)
        if name is None or banner is None or profile_pic is None or description is None:
            content = {
                'message': 'channel_name or banner or profile_pic or description  is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            if name.lstrip() == "":
                content = {
                    'message': 'name cannot be empty'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            new_channel = Channel.objects.create(
                name=name,
                banner=banner,
                profile_pic=profile_pic,
                description=description,
                subscribers=subscribers

            )
            new_channel.save()
            if new_channel.banner:
                banner_url = new_channel.banner.url
            else:
                banner_url = None
            if new_channel.profile_pic:
                profile_pic_url = new_channel.profile_pic.url
            else:
                profile_pic_url = None
            content = {
                'message': "new channel has been added",
                'data': {
                    'channel_id': new_channel.id,
                    'name': new_channel.name,
                    'banner': banner_url,
                    'profile_pic': profile_pic_url,
                    'description': new_channel.description,
                    'subscribers': new_channel.subscribers,
                    'created_at': new_channel.created_at,
                    'updated_at': new_channel.updated_at}
            }
            return Response(content, status=status.HTTP_201_CREATED)

        except Channel.DoesNotExist:
            content = {
                'message': 'channel_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            content = {
                'message': str(e)
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        # we can update the existing channel
        channel_id = request.POST.get("channel_id", None)
        new_name = request.POST.get('name', None)
        new_banner = request.FILES.get('banner', None)
        new_profile_pic = request.FILES.get('profile_pic', None)
        new_description = request.POST.get("description", None)
        new_subscribers = request.POST.get("subscribers", None)
        created_at = request.POST.get("created_at", None)
        updated_at = request.POST.get("updated_at", None)
        if channel_id is None:
            content = {
                'message': ' channel_id is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            if new_name is not None and new_name.lstrip() == "":
                content = {
                    'message': 'name cannot be empty'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            channel_info = Channel.objects.get(id=channel_id)
            channel_info.name = new_name if new_name is not None else channel_info.name
            channel_info.banner = new_banner if new_banner is not None else channel_info.banner
            channel_info.profile_pic = new_profile_pic if new_profile_pic is not None else channel_info.profile_pic
            channel_info.description = new_description if new_description is not None else channel_info.description
            channel_info.subscribers = new_subscribers if new_subscribers is not None else channel_info.subscribers
            channel_info.save()
            if channel_info.banner:
                banner_url = channel_info.banner.url
            else:
                banner_url = None
            if channel_info.profile_pic:
                profile_pic_url = channel_info.profile_pic.url
            else:
                profile_pic_url = None
            content = {
                'message': " channel has been updated",
                'data': {
                    'channel_id': channel_info.id,
                    'name': channel_info.name,
                    'banner_url': banner_url,
                    'profile_pic_url': profile_pic_url,
                    'description': channel_info.description,
                    'subscribers': channel_info.subscribers,
                    'created_at': channel_info.created_at,
                    'updated_at': channel_info.updated_at}

            }
            return Response(content, status=status.HTTP_200_OK)

        except Channel.DoesNotExist:
            content = {
                'message': 'channel_id  is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            content = {
                'message': str(e)
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # with this method, we can delete the channels, only it doesn't contain any videos
        channel_id = request.POST.get('channel_id', None)
        if channel_id is None:
            content = {
                'message': 'channel_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            channel_info = Channel.objects.get(id=channel_id)
            all_videos = Video.objects.filter(channel_id=channel_info.id)
            count = all_videos.count()
            if count > 0:
                content = {
                    "videos_count": count,
                    "message": "channel cannot be deleted, as it contain videos"
                }

                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                channel_info.delete()
                content = {
                    "message":"channel has been deleted"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Channel.DoesNotExist:
            content = {
                'message': 'channel_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            content = {
                'message': 'channel_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def video(request):
    if request.method == 'GET':
        # with this method, we can get single video
        video_id = request.GET.get('video_id', None)
        if video_id is None:
            content = {
                'message': 'video_id is missing'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            video_info = Video.objects.get(id=video_id)
            if video_info.thumbnail:
                image_url = video_info.thumbnail.url
            else:
                image_url = None
            if video_info.channel.profile_pic:
                profile_pic_url = video_info.channel.profile_pic.url
            else:
                profile_pic_url = None
            content = {
                'name': video_info.name,
                'description': video_info.description,
                'thumbnail': image_url,
                'likes': video_info.likes,
                'views': video_info.views,
                'channel_id': video_info.channel_id,
                'channel_name': video_info.channel.name,
                'channel_profile_image': profile_pic_url,
                'created_at': video_info.created_at,
                'updated_at': video_info.updated_at
            }
            return Response(content, status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            content = {
                'message': 'video_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            content = {
                'message': 'video_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        # with this method, we can add new video
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        channel_id = request.POST.get('channel_id', None)
        thumbnail = request.FILES.get('thumbnail', None)
        likes = request.POST.get("likes", None)
        views = request.POST.get("views", None)
        if name is None or description is None or channel_id is None or thumbnail is None:
            content = {
                'message': 'video_name or description or channel_id or thumbnail is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            if name.lstrip() == "":
                content = {
                    'message': 'name cannot be empty'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            new_video = Video.objects.create(
                channel_id=channel_id,
                name=name,
                description=description,
                thumbnail=thumbnail,
                likes=likes,
                views=views
            )
            new_video.save()
            if new_video.thumbnail:
                image_url = new_video.thumbnail.url
            else:
                image_url = None
            if new_video.channel.profile_pic:
                profile_pic_url = new_video.channel.profile_pic.url
            else:
                profile_pic_url = None
            content = {
                'message': "new video has been added",
                'data': {
                    'video_id': new_video.id,
                    'name': new_video.name,
                    'description': new_video.description,
                    'thumbnail': image_url,
                    'likes': new_video.likes,
                    'views': new_video.views,
                    'created_at': new_video.created_at,
                    'updated_at': new_video.updated_at,
                    'channel_id': new_video.channel_id,
                    'channel_name': new_video.channel.name,
                    'channel_profile': profile_pic_url
                }
            }
            return Response(content, status=status.HTTP_201_CREATED)

        except Video.DoesNotExist:
            content = {
                'message': 'video_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            content = {
                'message': str(e)
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            content = {
                'message': 'channel_id should be an integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        # with this method, we can update the existing videos
        video_id = request.POST.get("video_id", None)
        new_name = request.POST.get('name', None)
        new_description = request.POST.get('description', None)
        new_channel_id = request.POST.get('channel_id', None)
        new_thumbnail = request.FILES.get('thumbnail', None)
        new_likes = request.POST.get("likes", None)
        new_views = request.POST.get("views", None)
        if video_id is None:
            content = {
                'message': ' video_id is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            if new_name is not None and new_name.lstrip() == "":
                content = {
                    'message': 'name cannot be empty'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            video_info = Video.objects.get(id=video_id)
            video_info.name = new_name if new_name is not None else video_info.name
            video_info.description = new_description if new_description is not None else video_info.description
            video_info.channel_id = new_channel_id if new_channel_id is not None else video_info.channel_id
            video_info.thumbnail = new_thumbnail if new_thumbnail is not None else video_info.thumbnail
            video_info.likes = new_likes if new_likes is not None else video_info.likes
            video_info.views = new_views if new_views is not None else video_info.views
            video_info.save()
            if video_info.thumbnail:
                image_url = video_info.thumbnail.url
            else:
                image_url = None
            if video_info.channel.profile_pic:
                profile_pic_url = video_info.channel.profile_pic.url
            else:
                profile_pic_url = None
            content = {
                'message': " video has been updated",
                'data': {
                    'video_id': video_info.id,
                    'name': video_info.name,
                    'description': video_info.description,
                    'thumbnail': image_url,
                    'likes': video_info.likes,
                    'views': video_info.views,
                    'created_at': video_info.created_at,
                    'updated_at': video_info.updated_at,
                    'channel_id': video_info.channel_id,
                    'channel_name': video_info.channel.name,
                    'channel_profile': profile_pic_url}

            }
            return Response(content, status=status.HTTP_200_OK)

        except Video.DoesNotExist:
            content = {
                'message': 'video_id  is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            content = {
                'message': str(e)
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            content = {
                'message': 'channel_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # with this method, we can delete the video
        video_id = request.POST.get('video_id', None)
        if video_id is None:
            content = {
                'message': 'video_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            video_info = Video.objects.get(id=video_id)
            video_info.delete()
            content = {
                'message': 'video has been deleted'
            }
            return Response(content, status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            content = {
                'message': 'video_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            content = {
                'message': 'video_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def videos(request):
    channel_id = request.GET.get('channel_id', None)
    # with this method, we can get all the videos or else we can get the videos belong to the single channel
    if channel_id is None:
        all_videos = Video.objects.all()

    elif channel_id is not None:
        try:
            all_videos = Video.objects.filter(channel_id=channel_id)
        except ValueError:
            content = {
                'message': 'channel_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    final_videos = []
    for temp_video in all_videos:
        if temp_video.thumbnail:
            image_url = temp_video.thumbnail.url
        else:
            image_url = None
        if temp_video.channel.profile_pic:
            profile_pic_url = temp_video.channel.profile_pic.url
        else:
            profile_pic_url = None
        content = {
            'video_id': temp_video.id,
            'name': temp_video.name,
            'description': temp_video.description,
            'thumbnail': image_url,
            'likes': temp_video.likes,
            'views': temp_video.views,
            'created_at': temp_video.created_at,
            'updated_at': temp_video.updated_at,
            'channel_id': temp_video.channel_id,
            'channel_name': temp_video.channel.name,
            'channel_profile': profile_pic_url

        }
        final_videos.append(content)

    return Response(final_videos, status=status.HTTP_200_OK)
