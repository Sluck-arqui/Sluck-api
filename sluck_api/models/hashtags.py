from django.db import models


class Hashtag(models.Model):

  hashtag_text = models.TextField()

  def publish(self):
    self.save()


class MessageHashtag(models.Model):
  message_id = models.IntegerField()
  hashtag_id = models.IntegerField()

  def publish(self):
    self.save()