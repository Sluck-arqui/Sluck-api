from sluck_api.models import Message


def user_serializer(user):

  return {'id': user.id, 
          'username': user.username, 
          'email': user.email, 
          'first_name': user.first_name, 
          'last_name': user.last_name, 
          'created_at': user.created_at,
          'updated_at': user.updated_at}



def message_serializer(message, only_likes=False, limit=5):
  if only_likes:
    return {'likes': message.likes(),
            'like_authors': message.like_authors()[:limit]}
  else:
    return {'id': message.id,
            'text': message.text,
            'user_id': message.user_id,
            'group_id': message.group_id,
            'created_at': message.created_at,
            'updated_at': message.updated_at,
            'hashtags': message.hashtags(),
            'mentions': message.mentions(),
            'like_authors': message.like_authors()[:limit],
            'likes': message.likes()}


def group_serializer(group):
  return {'id': group.id,
          'name': group.name,
          'description': group.description,
          'members': group.members()}
