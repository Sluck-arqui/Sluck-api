from rest_framework import serializers
from .models import (
    User,
    Group,
    Hashtag,
    Message,
    ThreadMessage,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'email',
            'created_at',
            'updated_at',
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'description',
        )


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = (
            'id',
            'text',
            'messages',
            'thread_messages',
        )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'text',
            'author',
            'group',
            'hashtags',
            'mentions',
            'likers',
            'dislikers',
            'created_at',
            'updated_at',
        )


class ThreadMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadMessage
        fields = (
            'id',
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
