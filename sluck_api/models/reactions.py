from django.db import models


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

class ThreadLike(models.Model):

  user_id = models.IntegerField()
  message_id = models.IntegerField()

  def publish(self):
    self.save()

class ThreadDislike(models.Model): # O los unimos en uno y ponemos atributo 0: dislike, 1:like???

  user_id = models.IntegerField()
  message_id = models.IntegerField()

  def publish(self):
    self.save()