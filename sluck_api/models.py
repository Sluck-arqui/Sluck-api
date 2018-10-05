# from django.contrib.auth.models import User as DJUser
from django.db import models

# Create your models here.

class User(models.Model):
  username = models.TextField()
  first_name = models.TextField()
  last_name = models.TextField()
  password = models.TextField()
  email = models.EmailField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)

  def publish(self):
    self.save()


class Message(models.Model):
  text = models.TextField()
  user_id = models.IntegerField()
  group_id = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)

  def publish(self):
    hashtags_ = extract_tags(self.text, "#")
    for text in hashtags_:
      results = Hashtag.objects.filter(hashtag_text=text)
      if results.count() == 0:
        new_hashtag = Hashtag(hashtag_text=text)
        new_hashtag.save()
    self.save()

  def hashtags(self):
    hashtags_ = extract_tags(self.text, "#")
    hashtags = []
    for text in hashtags_:
      results = Hashtag.objects.filter(hashtag_text=text)
      if results.count() > 0:
        dicc = {'hashtag_id': results[0].id,
                'hashtag_text': results[0].hashtag_text}
        hashtags.append(dicc)
      else:
        new_hashtag = Hashtag(hashtag_text=text)
        new_hashtag.save()
        dicc = {'hashtag_id': new_hashtag.id,
                'hashtag_text': text}
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
    pass


class Hashtag(models.Model):

  hashtag_text = models.TextField()

  def publish(self):
    self.save()


class MessageLike(models.Model):

  user_id = models.IntegerField()
  message_id = models.IntegerField()

  def publish(self):
    self.save()

class MessageDislike(models.Model): # O los unimos en uno y ponemos atributo 0: dislike, 1:like???

  user_id = models.IntegerField()
  message_id = models.IntegerField()

  def publish(self):
    self.save()


class Group(models.Model):

  name = models.TextField()
  description = models.TextField()

  def publish(self):
    self.save()

  def members(self):
    users_groups_ = UserGroup.objects.filter(group_id=self.id)
    users = []
    for user in users_groups_:
      results = User.objects.filter(id=user.user_id)
      if results.count() > 0:
        dicc = {'user_id': results[0].id,
                'username': results[0].username}
        users.append(dicc)
    return users


class UserGroup(models.Model):

  user_id = models.IntegerField()
  group_id = models.IntegerField()

  def publish(self):
    self.save()

def extract_tags(s, division):
    return list(set(part[1:] for part in s.split() if part.startswith(division)))