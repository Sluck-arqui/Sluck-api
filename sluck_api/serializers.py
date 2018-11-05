from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils import timezone
from .models import (
    User,
    Group,
    Hashtag,
    Message,
    ThreadMessage,
)


class UserSerializer(serializers.ModelSerializer):
    """General usage user serializer"""
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
        )
        read_only_fields = (
            'created_at',
            'updated_at',
            'groups',
            'messages',
            'mentions',
        )

    def save(self, *args, **kwargs):
        instance = super(UserSerializer, self).save(*args, **kwargs)
        token = Token.objects.create(user=instance)
        return instance, token

    def get_token(self):
        token = Token.objects.get(user=self.instance)
        return token

    def new_token(self):
        Token.objects.filter(user=self.instance).delete()
        token = Token.objects.create(user=self.instance)
        return token


class UserUpdateSerializer(serializers.ModelSerializer):
    """Update only User serializer, allows only change of email and password"""
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
        )


class UserSecureSerializer(serializers.ModelSerializer):
    """Update only User serializer, allows only change of email and password"""
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'groups',
            'messages',
            'mentions',
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
    """General usage Group Serializer"""
    members = UserSummarySerializer(many=True, read_only=True)

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
    """General usage Hashtag Serializer"""
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


class ThreadMessageSerializer(serializers.ModelSerializer):
    """General usage for Creating and Showing Thread"""
    hashtags = HashtagSummarySerializer(many=True, read_only=True)
    mentions = UserSummarySerializer(many=True, read_only=True)
    likers = UserSummarySerializer(many=True, read_only=True)
    dislikers = UserSummarySerializer(many=True, read_only=True)

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
            'likes',
            'dislikes',
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
        )


class ThreadMessageUpdateSerializer(serializers.ModelSerializer):
    """Specific for Updating Threads. Only allows modifying text."""
    likers = UserSummarySerializer(many=True, read_only=True)
    dislikers = UserSummarySerializer(many=True, read_only=True)
    hashtags = HashtagSummarySerializer(many=True, read_only=True)
    mentions = UserSummarySerializer(many=True, read_only=True)

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
            'likes',
            'dislikes',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'author',
            'message',
            'mentions',
            'hashtags',
            'likers',
            'dislikers',
            'likes',
            'dislikes',
            'created_at',
            'updated_at',
        )


class ThreadMessageReactionsSerializer(serializers.ModelSerializer):
    """Specific for viewing a thread's reactions"""
    likers = UserSummarySerializer(many=True, read_only=True)
    dislikers = UserSummarySerializer(many=True, read_only=True)

    class Meta:
        model = ThreadMessage
        fields = (
            'id',
            'likers',
            'dislikers',
            'likes',
            'dislikes',
        )
        read_only_fields = (
            'id',
            'likers',
            'dislikers',
            'likes',
            'dislikes',
        )



class MessageSerializer(serializers.ModelSerializer):
    """General usage for Creating and Showing Message"""
    hashtags = HashtagSummarySerializer(many=True, read_only=True)
    mentions = UserSummarySerializer(many=True, read_only=True)
    likers = UserSummarySerializer(many=True, read_only=True)
    dislikers = UserSummarySerializer(many=True, read_only=True)
    threads = ThreadMessageSerializer(many=True, read_only=True)

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
    """Specific for Updating Messages. Only allows modifying text."""
    likers = UserSummarySerializer(many=True, read_only=True)
    dislikers = UserSummarySerializer(many=True, read_only=True)
    hashtags = HashtagSummarySerializer(many=True, read_only=True)
    mentions = UserSummarySerializer(many=True, read_only=True)
    threads = ThreadMessageSerializer(many=True, read_only=True)

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


class MessageReactionsSerializer(serializers.ModelSerializer):
    """Specific for viewing a message's reactions"""
    likers = UserSummarySerializer(many=True, read_only=True)
    dislikers = UserSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = (
            'id',
            'likers',
            'dislikers',
            'likes',
            'dislikes',
        )
        read_only_fields = (
            'id',
            'likers',
            'dislikers',
            'likes',
            'dislikes',
        )



### PERHAPS USE THIS LATER FOR HIGHER CUSTOMIZATION ###
# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     first_name = serializers.CharField(required=True)
#     last_name = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)
#     email = serializers.EmailField(required=True)
#
#     def create(self, validated_data):
#         return User.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.password = validated_data.get('password', instance.password)
#         instance.email = validated_data.get('email', instance.email)
#         instance.save()
#         return instance
