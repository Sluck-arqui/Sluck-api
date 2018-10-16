from django.db import models
from django.contrib.auth.models import AbstractUser
from encrypted_model_fields.fields import EncryptedCharField
from .utils import extract_tags


class User(AbstractUser):
    username = models.TextField(unique=True)
    first_name = models.TextField()
    last_name = models.TextField()
    password = EncryptedCharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.save()


class Group(models.Model):

    name = models.TextField()
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='g')

    def publish(self):
        self.save()


class Hashtag(models.Model):
    text = models.TextField(unique=True)

    def publish(self):
        self.save()


class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='messages',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        related_name='messages',
        on_delete=models.CASCADE,
    )
    mentions = models.ManyToManyField(User, related_name='mentions')
    hashtags = models.ManyToManyField(Hashtag, related_name='messages')
    likers = models.ManyToManyField(User, related_name='liked_messages')
    dislikers = models.ManyToManyField(User, related_name='disliked_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes(self):
        return self.likers.count()

    @property
    def dislikes(self):
        return self.dislikers.count()

    def publish(self):
        self.save()
        new_hashtags_texts = extract_tags(self.text, '#')
        new_hashtags = []
        for hashtag_text in new_hashtags_texts:
            hashtag = Hashtag.objects.filter(text=hashtag_text)
            if hashtag:
                new_hashtags.append(hashtag[0])
            else:
                new_hashtags.append(Hashtag.objects.create(text=hashtag_text))
        self.hashtags.set(new_hashtags)
        new_mentions_usernames = extract_tags(self.text, '@')
        new_mentions = []
        for username in new_mentions_usernames:
            user = User.objects.filter(username=username)
            if user:
                new_mentions.append(user[0])
        self.mentions.set(new_mentions)
        return self


class ThreadMessage(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='threads',
        on_delete=models.CASCADE,
    )
    message = models.ForeignKey(
        Message,
        related_name='threads',
        on_delete=models.CASCADE,
    )
    mentions = models.ManyToManyField(User, related_name='thread_mentions')
    hashtags = models.ManyToManyField(Hashtag, related_name='thread_messages')
    likers = models.ManyToManyField(User, related_name='liked_threads')
    dislikers = models.ManyToManyField(User, related_name='disliked_threads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes(self):
        return self.likers.count()

    @property
    def dislikes(self):
        return self.dislikers.count()

    def publish(self):
        self.save()
        new_hashtags_texts = extract_tags(self.text, '#')
        new_hashtags = []
        for hashtag_text in new_hashtags_texts:
            hashtag = Hashtag.objects.filter(text=hashtag_text)
            if hashtag:
                new_hashtags.append(hashtag[0])
            else:
                new_hashtags.append(Hashtag.objects.create(text=hashtag_text))
        self.hashtags.set(new_hashtags)
        new_mentions_usernames = extract_tags(self.text, '@')
        new_mentions = []
        for username in new_mentions_usernames:
            user = User.objects.filter(username=username)
            if user:
                new_mentions.append(user[0])
        self.mentions.set(new_mentions)
        return self
