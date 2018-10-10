from rest_framework import serializers
from .models import (
    User,
    Group,
    Hashtag,
    Message,
    ThreadMessage,
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password',
            'email',
            'threads',
            'messages',
            'groups',
            'mentions',
            'liked_messages',
            'disliked_messages',
            'liked_threads',
            'disliked_threads',
            'created_at',
            'updated_at',
        )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = (
            'name',
            'description',
            'messages',
            'members',
        )


class HashtagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hashtag
        fields = (
            'text',
            'messages',
            'thread_messages',
        )


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = (
            'text',
            'author',
            'group',
            'mentions',
            'hashtags',
            'likers',
            'dislikers',
            'created_at',
            'updated_at',
        )


class ThreadMessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ThreadMessage
        fields = (
            'text',
            'author',
            'message',
            'mentions',
            'hashtags',
            'likers',
            'dislikers',
            'created_at',
            'updated_at',
        )
