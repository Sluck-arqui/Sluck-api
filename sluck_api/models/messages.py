from django.db import models
from sluck_api.serializers import thread_serializer
from .hashtags import Hashtag, MessageHashtag
from .reactions import MessageLike, MessageDislike, ThreadLike, ThreadDislike
from .users import User


class Message(models.Model):
  text = models.TextField()
  user_id = models.IntegerField()
  group_id = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)

  def publish(self, edit=False):
    if edit:
      my_hashtags = self.hashtags()
      my_hashtags = [h['hashtag_text'] for h in my_hashtags]
    self.save()
    hashtags_ = extract_tags(self.text, "#")
    if not edit:
      for text in hashtags_:
        results = Hashtag.objects.filter(hashtag_text=text)
        if results.count() == 0:
          new_hashtag = Hashtag(hashtag_text=text)
          new_hashtag.publish()
          message_hashtag = MessageHashtag(message_id=self.id,
                                           hashtag_id=new_hashtag.id)
          message_hashtag.publish()
        else:
          hashtag = results[0]
          message_hashtag = MessageHashtag(message_id=self.id,
                                           hashtag_id=hashtag.id)
          message_hashtag.publish()
    else:
      for text in hashtags_:
        if text not in my_hashtags:
          new_hashtag = Hashtag(hashtag_text=text)
          new_hashtag.publish()
          message_hashtag = MessageHashtag(message_id=self.id,
                                           hashtag_id=new_hashtag.id)
          message_hashtag.publish()

  def hashtags(self):
    hashtags = []
    results = MessageHashtag.objects.filter(message_id=self.id)
    for message_hashtag in results:
      hashtag = Hashtag.objects.filter(id=message_hashtag.hashtag_id)[0]
      dicc = {'hashtag_id': hashtag.id,
              'hashtag_text': hashtag.hashtag_text}
      hashtags.append(dicc)
    return hashtags

  def mentions(self):
    users_ = extract_tags(self.text, "@")
    users = []
    for user in users_:
      results = User.objects.filter(username=user)
      if results.count() > 0:
        dicc = {'user_id': results[0].id,
                'username': results[0].username}
        users.append(dicc)
    return users

  def likes(self):
    return len(self.like_authors())

  def like_authors(self):
    likes_ = MessageLike.objects.filter(message_id=self.id)
    users = []
    for like in likes_:
      results = User.objects.filter(id=like.user_id)
      if results.count() > 0:
        dicc = {'user_id': results[0].id,
                'username': results[0].username}
        users.append(dicc)
    return users

  def dislikes(self):
    return len(self.dislike_authors())

  def dislike_authors(self):
    dislikes_ = MessageDislike.objects.filter(message_id=self.id)
    users = []
    for dislike in dislikes_:
      results = User.objects.filter(id=dislike.user_id)
      if results.count() > 0:
        dicc = {'user_id': results[0].id,
                'username': results[0].username}
        users.append(dicc)
    return users

  def threads(self):
    comments_ = ThreadMessage.objects.filter(message_id=self.id)
    comments = []
    for comment in comments_:
      comments.append(thread_serializer(comment))
    return comments


class ThreadMessage(models.Model):
  text = models.TextField()
  user_id = models.IntegerField()
  message_id = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)

  def publish(self):
    self.save()

  def mentions(self):
    users_ = extract_tags(self.text, "@")
    users = []
    for user in users_:
      results = User.objects.filter(username=user)
      if results.count() > 0:
        dicc = {'user_id': results[0].id,
                'username': results[0].username}
        users.append(dicc)
    return users

  def likes(self):
    return len(self.like_authors())

  def like_authors(self):
    likes_ = ThreadLike.objects.filter(message_id=self.id)
    users = []
    for like in likes_:
      results = User.objects.filter(id=like.user_id)
      if results.count() > 0:
        dicc = {'user_id': results[0].id,
                'username': results[0].username}
        users.append(dicc)
    return users

  def dislikes(self):
    return len(self.dislike_authors())

  def dislike_authors(self):
    dislikes_ = ThreadDislike.objects.filter(message_id=self.id)
    users = []
    for dislike in dislikes_:
      results = User.objects.filter(id=dislike.user_id)
      if results.count() > 0:
        dicc = {'user_id': results[0].id,
                'username': results[0].username}
        users.append(dicc)
    return users

  def threads(self):
    return []



def extract_tags(s, division):
    return list(set(part[1:] for part in s.split() if part.startswith(division)))