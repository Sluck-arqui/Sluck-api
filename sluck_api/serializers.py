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
            'groups',
            'messages',
            'mentions',
            'liked_messages',
            'liked_threads',
            'disliked_messages',
            'disliked_threads',
        )
        read_only_fields = (
            'created_at',
            'updated_at',
            'groups',
            'messages',
            'mentions',
            'liked_messages',
            'liked_threads',
            'disliked_messages',
            'disliked_threads',
        )


class UserUpdateSerializer(serializers.ModelSerializer):
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
            'groups',
            'messages',
            'mentions',
            'liked_messages',
            'liked_threads',
            'disliked_messages',
            'disliked_threads',
        )
        read_only_fields = (
            'username',
            'first_name',
            'last_name',
            'created_at',
            'updated_at',
            'groups',
            'messages',
            'mentions',
            'liked_messages',
            'liked_threads',
            'disliked_messages',
            'disliked_threads',
        )


class UserSummarySerializer(serializers.ModelSerializer):
    """Summarized version for showing User Objects Within Other Objects"""
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )
        read_only_fields = (
            'id',
            'username',
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'description',
            'members',
            'messages',
        )
        read_only_fields = ('id', 'members', 'messages')
        # extra_kwargs = {
        #     'security_question': {'write_only': True},
        #     'security_question_answer': {'write_only': True},
        #     'password': {'write_only': True}
        # }


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = (
            'id',
            'text',
            'messages',
            'thread_messages',
        )
        read_only_fields = ('messages', 'thread_messages')


class HashtagSummarySerializer(serializers.ModelSerializer):
    """Summarized version for showing Hashtag Objects Within Other Objects"""
    class Meta:
        model = Hashtag
        fields = (
            'id',
            'text',
        )


class MessageSerializer(serializers.ModelSerializer):
    hashtags = HashtagSummarySerializer(many=True, read_only=True)
    mentions = UserSummarySerializer(many=True, read_only=True)

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
            'likes',
            'dislikes',
            'threads',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'hashtags',
            'mentions',
            'likers',
            'dislikers',
            'likes',
            'dislikes',
            'threads',
        )

    def create(self, validated_data):
        print("yep")
        instance = super().create(validated_data)
        return instance.publish()


class MessageUpdateSerializer(serializers.ModelSerializer):
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
            'likes',
            'dislikes',
            'threads',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'author',
            'group',
            'hashtags',
            'mentions',
            'likers',
            'dislikers',
            'likes',
            'dislikes',
            'threads',
            'created_at',
            'updated_at',
        )

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        instance.publish()
        return instance


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
        read_only_fields = (
            'hashtags',
            'mentions',
            'likers',
            'dislikers',
        )


class ThreadMessageUpdateSerializer(serializers.ModelSerializer):
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
        read_only_fields = (
            'id',
            'author',
            'message',
            'hashtags',
            'mentions',
            'likers',
            'dislikers',
            'threads',
            'created_at',
            'updated_at',
        )
