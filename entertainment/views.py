from django.shortcuts import render
from .models import CustomUser, Channel, Video, Comment
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError


# Create your views here.
@api_view(['POST'])
def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        confirm_password = request.POST.get("confirm_password", None)
        if username is None or password is None or confirm_password is None:
            content = {
                'message': 'username or password or category_id or confirm_password  is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if "-" in username or "@" in username or "#" in username or "*" in username or "&" in username:
            content = {
                "message": "special symbols cannot be used for usernames"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if username.isalpha() is not True or username.lstrip() == "":
            content = {
                "message": "name cannot be empty or spacing is not allowed or name cannot be number"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:

                new_user = CustomUser.objects.create_user(username=username, password=password)
                new_user.save()
                content = {
                    'message': "new user is added",
                    'username': new_user.username,
                    "user_id": new_user.id

                }
                return Response(content, status=status.HTTP_201_CREATED)
            except IntegrityError:
                content = {
                    'message': 'user already exists'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def channel(request):
    # with this method, we can get the single channel
    if request.method == 'GET':
        channel_id = request.GET.get('channel_id', None)
        user_id = request.user.id
        if channel_id is None:
            content = {
                'message': 'channel_id is missing'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            channel_info = Channel.objects.get(id=channel_id, user_id=user_id)
            if channel_info.banner:
                banner_url = channel_info.banner.url
            else:
                banner_url = None
            if channel_info.profile_pic:
                image_url = channel_info.profile_pic.url
            else:
                image_url = None
            content = {
                'user': user_id,
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
        user_id = request.user
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
                subscribers=subscribers,
                user_id=user_id

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
                    'user_id': user_id.id,
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
        user_id = request.user.id

        if channel_id is None:
            content = {
                'message': ' channel_id is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if new_name is not None and new_name.lstrip() == "":
            content = {
                'message': 'name cannot be empty'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            channel_info = Channel.objects.get(id=channel_id, user_id=user_id)
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
                    'user_id': user_id,
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
            channel_info = Channel.objects.get(id=channel_id, user_id=request.user)
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
                    "message": "channel has been deleted"
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


@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def video(request):
    if request.method == 'GET':
        # with this method, we can get single video
        video_id = request.GET.get('video_id', None)
        user_id = request.user.id
        if video_id is None:
            content = {
                'message': 'video_id is missing'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            video_info = Video.objects.get(id=video_id, user_id=user_id)
            if video_info.thumbnail:
                image_url = video_info.thumbnail.url
            else:
                image_url = None
            if video_info.channel.profile_pic:
                profile_pic_url = video_info.channel.profile_pic.url
            else:
                profile_pic_url = None
            content = {
                'user': user_id,
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
        user_id = request.user.id
        if name is None or description is None or channel_id is None or thumbnail is None:
            content = {
                'message': 'video_name or description or channel_id or thumbnail is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if name.lstrip() == "":
            content = {
                'message': 'name cannot be empty'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            channel_info = Channel.objects.get(id=channel_id, user_id=user_id)
            new_video = Video.objects.create(
                channel_id=channel_id,
                name=name,
                description=description,
                thumbnail=thumbnail,
                likes=likes,
                views=views,
                user_id=channel_info.user_id
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
                    'user_id': user_id,
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
        except Channel.DoesNotExist:
            content = {
                'message': 'channel_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        # with this method, we can update the existing videos
        video_id = request.POST.get("video_id", None)
        new_name = request.POST.get('name', None)
        new_description = request.POST.get('description', None)
        channel_id = request.POST.get('channel_id', None)
        new_thumbnail = request.FILES.get('thumbnail', None)
        new_likes = request.POST.get("likes", None)
        new_views = request.POST.get("views", None)
        user_id = request.user.id
        if video_id is None:
            content = {
                'message': ' video_id is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if new_name is not None and new_name.lstrip() == "":
            content = {
                'message': 'name cannot be empty'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            video_info = Video.objects.get(id=video_id, user_id=user_id)
            video_info.name = new_name if new_name is not None else video_info.name
            video_info.description = new_description if new_description is not None else video_info.description
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
                    'user_id': user_id,
                    'video_id': video_info.id,
                    'name': video_info.name,
                    'description': video_info.description,
                    'thumbnail': image_url,
                    'likes': video_info.likes,
                    'views': video_info.views,
                    'created_at': video_info.created_at,
                    'updated_at': video_info.updated_at,
                    'channel_id': video_info.channel.id,
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
        user_id = request.user.id
        if video_id is None:
            content = {
                'message': 'video_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            video_info = Video.objects.get(id=video_id, user_id=user_id)
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


@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def comment(request):
    if request.method == 'GET':
        # with this method, we can get the required comment
        comment_id = request.GET.get('comment_id', None)
        user_id = request.user.id
        if comment_id is None:
            content = {
                'message': 'comment_id is missing'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            comment_info = Comment.objects.get(id=comment_id, user_id=user_id)

            if comment_info.commenter_image:
                image_url = comment_info.commenter_image.url
            else:
                image_url = None
            if comment_info.video.channel.profile_pic:
                profile_pic_url = comment_info.video.channel.profile_pic.url
            else:
                profile_pic_url = None
            content = {
                'user_id': user_id,
                'video_id': comment_info.video_id,
                'video_name': comment_info.video.name,
                'channel_id': comment_info.video.channel_id,
                'channel_name': comment_info.video.channel.name,
                'channel_profile': profile_pic_url,
                'commenter_name': comment_info.commenter_name,
                'commenter_image': image_url,
                'comment': comment_info.comment,
                'likes': comment_info.likes,
                'created_at': comment_info.created_at,
                'updated_at': comment_info.updated_at
            }
            return Response(content, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            content = {
                'message': 'comment_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            content = {
                'message': 'comment_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        # with this method,we can add new comment
        video_id = request.POST.get("video_id", None)
        commenter_name = request.POST.get('commenter_name', None)
        commenter_image = request.FILES.get("commenter_image", None)
        comment = request.POST.get("comment", None)
        likes = request.POST.get("likes", None)
        user_id = request.user.id
        if video_id is None or commenter_name is None or commenter_image is None or comment is None:
            content = {
                'message': 'video_id or commenter_name or commenter_image or comment is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            video_info = Video.objects.get(id=video_id, user_id=user_id)
            new_comment = Comment.objects.create(
                video_id=video_id,
                commenter_name=commenter_name,
                commenter_image=commenter_image,
                comment=comment,
                likes=likes,
                user_id=video_info.user_id

            )
            new_comment.save()
            if new_comment.commenter_image:
                image_url = new_comment.commenter_image.url
            else:
                image_url = None
            if new_comment.video.channel.profile_pic:
                profile_pic_url = new_comment.video.channel.profile_pic.url
            else:
                profile_pic_url = None
            content = {
                'message': "new comment has been added",
                'data': {
                    'user_id': user_id,
                    'video_id': new_comment.video_id,
                    'video_name': new_comment.video.name,
                    'channel_id': new_comment.video.channel_id,
                    'channel_name': new_comment.video.channel.name,
                    'channel_profile': profile_pic_url,
                    'commenter_name': new_comment.commenter_name,
                    'commenter_image': image_url,
                    'comment': new_comment.comment,
                    'likes': new_comment.likes,
                    'created_at': new_comment.created_at,
                    'updated_at': new_comment.updated_at
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
    elif request.method == 'PATCH':
        # with this method, we can update the existing videos
        comment_id = request.POST.get("comment_id", None)
        video_id = request.POST.get("video_id", None)
        new_commenter_name = request.POST.get('commenter_name', None)
        new_commenter_image = request.FILES.get("commenter_image", None)
        new_comment = request.POST.get("comment", None)
        new_likes = request.POST.get("likes", None)
        user_id = request.user.id
        if comment_id is None:
            content = {
                'message': ' comment_id is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            if new_commenter_name is not None and new_commenter_name.lstrip() == "":
                content = {
                    'message': 'name cannot be empty'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            comment_info = Comment.objects.get(id=comment_id, user_id=user_id)
            comment_info.commenter_name = new_commenter_name if new_commenter_name is not None \
                else comment_info.commenter_name
            comment_info.commenter_image = new_commenter_image if new_commenter_image is not None \
                else comment_info.commenter_image
            comment_info.comment = new_comment if new_comment is not None else comment_info.comment
            comment_info.likes = new_likes if new_likes is not None else comment_info.likes

            comment_info.save()
            if comment_info.commenter_image:
                image_url = comment_info.commenter_image.url
            else:
                image_url = None
            if comment_info.video.channel.profile_pic:
                profile_pic_url = comment_info.video.channel.profile_pic.url
            else:
                profile_pic_url = None

            content = {
                'message': " comment has been updated",
                'data': {
                    'user_id': user_id,
                    'video_id': comment_info.video_id,
                    'video_name': comment_info.video.name,
                    'channel_id': comment_info.video.channel_id,
                    'channel_name': comment_info.video.channel.name,
                    'channel_profile': profile_pic_url,
                    'commenter_name': comment_info.commenter_name,
                    'commenter_image': image_url,
                    'comment': comment_info.comment,
                    'likes': comment_info.likes,
                    'created_at': comment_info.created_at,
                    'updated_at': comment_info.updated_at}

            }
            return Response(content, status=status.HTTP_200_OK)

        except Comment.DoesNotExist:
            content = {
                'message': 'comment_id  is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            content = {
                'message': str(e)
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            content = {
                'message': 'video_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # with this method, we can delete the existing comment
        comment_id = request.POST.get('comment_id', None)
        user_id = request.user.id
        if comment_id is None:
            content = {
                'message': 'comment_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            comment_info = Comment.objects.get(id=comment_id, user_id=user_id)
            comment_info.delete()
            content = {
                'message': 'comment has been deleted'
            }
            return Response(content, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            content = {
                'message': 'comment_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            content = {
                'message': 'comment_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def videos(request):
    channel_id = request.GET.get('channel_id', None)
    user_id = request.user.id
    # with this method, we can get all the videos or else we can get the videos belong to the single channel
    if channel_id is None:
        all_videos = Video.objects.filter(user_id=user_id)

    elif channel_id is not None:
        try:
            all_videos = Video.objects.filter(channel_id=channel_id, user_id=user_id)

        except ValueError:
            content = {
                'message': 'channel_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Video.DoesNotExist:
            content = {
                'message': 'videos not found'
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
            'user_id': user_id,
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


@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def comments(request):
    video_id = request.GET.get('video_id', None)
    user_id = request.user.id
    # with this method, we can get all the comments or else we can get the comments belong to the single video
    if video_id is None:
        all_comments = Comment.objects.all(user_id=user_id)

    elif video_id is not None:
        try:
            all_comments = Comment.objects.filter(video_id=video_id, user_id=user_id)
        except ValueError:
            content = {
                'message': 'video_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    final_comments = []
    for temp_comment in all_comments:
        if temp_comment.commenter_image:
            image_url = temp_comment.commenter_image.url
        else:
            image_url = None
        if temp_comment.video.channel.profile_pic:
            profile_pic_url = temp_comment.video.channel.profile_pic.url
        else:
            profile_pic_url = None
        content = {
            'user_id': user_id,
            'video_id': temp_comment.video_id,
            'video_name': temp_comment.video.name,
            'channel_id': temp_comment.video.channel_id,
            'channel_name': temp_comment.video.channel.name,
            'channel_profile': profile_pic_url,
            'commenter_name': temp_comment.commenter_name,
            'commenter_image': image_url,
            'comment': temp_comment.comment,
            'likes': temp_comment.likes,
            'created_at': temp_comment.created_at,
            'updated_at': temp_comment.updated_at

        }
        final_comments.append(content)

    return Response(final_comments, status=status.HTTP_200_OK)
