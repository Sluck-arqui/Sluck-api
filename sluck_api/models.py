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

  class Meta:
    ordering = ('created_at',)


class Message(models.Model):
  text = models.TextField()
  user_id = models.IntegerField()
  group_id = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)

  def publish(self):
    self.save()

  def hashtags(self):
    return extract_tags(self.text, "#")

  def mentions(self):
    return extract_tags(self.text, "@")

  class Meta:
    ordering = ('created_at',)



def extract_tags(s, division):
    return list(set(part[1:] for part in s.split() if part.startswith(division)))