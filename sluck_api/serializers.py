from sluck_api.models import Message


def user_serializer(User):

  return {'id': User.id, 
          'username': User.username, 
          'email': User.email, 
          'first_name': User.first_name, 
          'last_name': User.last_name, 
          'created_at': User.created_at,
          'updated_at': User.updated_at}



def message_serializer(Message):
  return {'id': Message.id,
          'text': Message.text,
          'user_id': Message.user_id,
          'group_id': Message.group_id,
          'created_at': Message.created_at,
          'updated_at': Message.updated_at,
          'hashtags': Message.hashtags(),
          'mentions': Message.mentions()}

