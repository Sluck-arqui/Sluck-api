from rest_framework import serializers
from .models import (
    User,
    Group,
    Hashtag,
    Message,
    ThreadMessage,
)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


#
# def user_serializer(user):
#
#   return {'id': user.id,
#           'username': user.username,
#           'email': user.email,
#           'first_name': user.first_name,
#           'last_name': user.last_name,
#           'created_at': user.created_at,
#           'updated_at': user.updated_at}
#
#
#
# def message_serializer(message, only_likes=False, limit=5):
#   if only_likes:
#     return {'likes': message.likes(),
#             'like_authors': message.like_authors()[:limit],
#             'dislikes': message.dislikes(),
#             'dislike_authors': message.dislike_authors()[:limit]}
#   else:
#     return {'id': message.id,
#             'text': message.text,
#             'user_id': message.user_id,
#             'group_id': message.group_id,
#             'created_at': message.created_at,
#             'updated_at': message.updated_at,
#             'hashtags': message.hashtags(),
#             'mentions': message.mentions(),
#             'like_authors': message.like_authors()[:limit],
#             'likes': message.likes(),
#             'dislike_authors': message.dislike_authors()[:limit],
#             'dislikes': message.dislikes(),
#             'threads': message.threads()}
#
# def thread_serializer(thread, only_likes=False, limit=5):
#   if only_likes:
#     return {'likes': thread.likes(),
#             'like_authors': thread.like_authors()[:limit]}
#   else:
#     return {'id': thread.id,
#             'text': thread.text,
#             'user_id': thread.user_id,
#             'message_id': thread.message_id,
#             'created_at': thread.created_at,
#             'updated_at': thread.updated_at,
#             'mentions': thread.mentions(),
#             'like_authors': thread.like_authors()[:limit],
#             'likes': thread.likes(),
#             'dislike_authors': thread.dislike_authors()[:limit],
#             'dislikes': thread.dislikes(),
#             'threads': thread.threads()}
#
#
# def group_serializer(group):
#   return {'id': group.id,
#           'name': group.name,
#           'description': group.description,
#           'members': group.members()}
