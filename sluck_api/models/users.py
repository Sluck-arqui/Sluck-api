from django.db import models


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