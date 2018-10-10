# from .serializers import UserSerializer, user_serializer, message_serializer, group_serializer, thread_serializer
from .serializers import (
    UserSerializer,
    GroupSerializer,
    HashtagSerializer,
    MessageSerializer,
    ThreadMessageSerializer,
)
from rest_framework import viewsets
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Message, User, Group, Hashtag, ThreadMessage
import datetime
import json


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class HashtagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = GroupSerializer


class ThreadMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ThreadMessage.objects.all()
    serializer_class = UserSerializer


#
#
# @csrf_exempt
# def users(request):
#     """
#     List all users, or create a new user.
#     """
#     if request.method == 'GET':
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def register(request):
#     """
#     List all users, or create a new user.
#     """
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=401)
#     else:
#         return JsonResponse({'status_text': 'Unauthorized'}, status=401)
#
#
# @csrf_exempt
# def get_user(request):
#     if request.method == 'GET':
#         if request.body:
#             data = JSONParser().parse(request)
#             user_id = data.get('user_id', None)
#             if user_id:
#                 user = User.objects.filter(id=user_id)
#                 if user:
#                     serializer = UserSerializer(user)
#                     return JsonResponse(serializer.data, safe=False)
#         return JsonResponse(
#             {'status_text': 'Object user not found.'}, status=404)
#
#     elif request.method == 'PATCH':
#         data = JSONParser().parse(request)
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         data = JSONParser().parse(request)
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#     else:
#         return JsonResponse({'status_text': 'Unauthorized'}, status=401)
#
#
# # Por ahora http://127.0.0.1:8000/user/?user_id=1
# # requests.get(url, params={'user_id':1})
# def get_user2(request):
#     if request.method == 'GET':
#         try:
#             user_id = request.GET.get('user_id')
#             users = User.objects.filter(id=user_id)
#             user = users[0]
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object user not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 200, 'status_text':'Ok', 'user': user_serializer(user)},
#             json_dumps_params={'indent': 2})
#     elif request.method == 'DELETE':
#         try:
#             data = json.loads(request.body)
#             user_id = data.get('user_id')
#             users = User.objects.filter(id=user_id)
#             user = users[0]
#             user.delete()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object user not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 200, 'status_text':'Deleted successfully'},
#             json_dumps_params={'indent': 2})
#     elif request.method == 'PATCH':
#         try:
#             data = json.loads(request.body)
#             user_id = data.get('user_id')
#             users = User.objects.filter(id=user_id)
#             user = users[0]
#             mail = data.get('email')
#             password = data.get('password')
#             user.email = mail
#             user.password = password
#             user.updated_at = datetime.datetime.now()
#             user.publish()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object user not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 200, 'status_text':'Updated successfully', 'user': user_serializer(user)},
#             json_dumps_params={'indent': 2})
#     else:
#         return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'},
#                             json_dumps_params={'indent': 2})
#
#
#
# # http://127.0.0.1:8000/group/?group_id=1
# # requests.get(url, params={'group_id':1})
# def get_group(request):
#     if request.method == 'GET':
#         try:
#             group_id = request.GET.get('group_id')
#             groups = Group.objects.filter(id=group_id)
#             group = groups[0]
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 200, 'status_text':'Ok', 'group': group_serializer(group)},
#             json_dumps_params={'indent': 2})
#     elif request.method == 'DELETE':
#         try:
#             data = json.loads(request.body)
#             group_id = data.get('group_id')
#             groups = Group.objects.filter(id=group_id)
#             group = groups[0]
#             group.delete()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 200, 'status_text':'Deleted successfully'},
#             json_dumps_params={'indent': 2})
#     else:
#         return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'},
#                             json_dumps_params={'indent': 2})
#
#
# # requests.post(url, data={'name':'Second group', 'description':'This is the second group'})
# def new_group(request):
#     if request.method == 'POST':
#         try:
#             name = request.POST.get('name')
#             description = request.POST.get('description')
#             group = Group(name=name, description=description)
#             group.publish()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 400, 'status_text': 'Bad request.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 201, 'status_text':'Created successfully',
#             'group': group_serializer(group)}, json_dumps_params={'indent': 2})
#     else:
#         return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'},
#                             json_dumps_params={'indent': 2})
#
#
# # requests.post(url, data={'group_id':3, 'user_id':1})
# def group_member(request):
#     if request.method == 'POST':
#         try:
#             group_id = request.POST.get('group_id')
#             user_id = request.POST.get('user_id')
#             groups = Group.objects.filter(id=group_id)
#             group = groups[0]
#             new_member = UserGroup(user_id=user_id, group_id=group_id)
#             new_member.publish()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 200, 'status_text':'Added successfully',
#             'group': group_serializer(group)}, json_dumps_params={'indent': 2})
#     elif request.method == 'DELETE':
#         # requests.delete(url, params={'group_id':3, 'user_id':1})
#         try:
#             data = json.loads(request.body)
#             group_id = data.get('group_id')
#             user_id = data.get('user_id')
#             groups = Group.objects.filter(id=group_id)
#             group = groups[0]
#             new_member = UserGroup.objects.filter(user_id=user_id, group_id=group_id)
#             new_member.delete()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object group or user not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 200, 'status_text':'Deleted successfully'},
#                             json_dumps_params={'indent': 2})
#     else:
#         return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'},
#                             json_dumps_params={'indent': 2})
#
#
#
# # Por ahora http://127.0.0.1:8000/message/?message_id=1
# # requests.get(url, params={'message_id':1})
# def get_message(request):
#     if request.method == 'GET':
#         try:
#             message_id = request.GET.get('message_id')
#             messages = Message.objects.filter(id=message_id)
#             message = messages[0]
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 200, 'status_text':'Ok', 'message': message_serializer(message)},
#             json_dumps_params={'indent': 2})
#     elif request.method == 'DELETE':
#         # requests.delete(url, data=json.dumps({'message_id':5}))
#         try:
#             data = json.loads(request.body)
#             message_id = data.get('message_id')
#             messages = Message.objects.filter(id=message_id)
#             message = messages[0]
#             message.delete()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 200, 'status_text':'Deleted successfully'},
#             json_dumps_params={'indent': 2})
#     elif request.method == 'PATCH':
#         try:
#             data = json.loads(request.body)
#             message_id = data.get('message_id')
#             new_text = data.get('text')
#             results = Message.objects.filter(id=message_id)
#             message = results[0]
#             message.text = new_text
#             message.updated_at = datetime.datetime.now()
#             message.publish(edit=True)
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 201, 'status_text':'Updated successfully',
#             'message': message_serializer(message)}, json_dumps_params={'indent': 2})
#     else:
#         return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'},
#                             json_dumps_params={'indent': 2})
#
#
# # requests.post(url, data={'group_id':1, 'text':'Estoy feliz #Happy #VivaLaVida'})
# def post_message(request):
#     if request.method == 'POST':
#         try:
#             group_id = request.POST.get('group_id')
#             text = request.POST.get('text')
#             results = Group.objects.filter(id=group_id)
#             group = results[0]
#             new_message = Message(group_id=group_id, text=text, user_id=2)
#             # Por mientras usuario 1, luego se revisa con los headers y las keys
#             new_message.publish()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 201, 'status_text':'Created successfully',
#             'message': message_serializer(new_message)}, json_dumps_params={'indent': 2})
#     elif request.method == 'GET':
#         try:
#             group_id = request.GET.get('group_id')
#             results = Group.objects.filter(id=group_id)
#             group = results[0]
#             messages_ = Message.objects.filter(group_id=group_id)
#             messages = []
#             for message in messages_:
#                 messages.append(message_serializer(message))
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 200, 'status_text':'Ok', 'message': messages},
#             json_dumps_params={'indent': 2})
#     else:
#         return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'},
#                             json_dumps_params={'indent': 2})
#
#
# # requests.post(url, data={'message_id':3})
# def like_message(request):
#     if request.method == 'POST':
#         try:
#             message_id = request.POST.get('message_id')
#             results = Message.objects.filter(id=message_id)
#             message = results[0]
#             new_like = MessageLike(message_id=message_id, user_id=1)
#             # Por mientras usuario 1, luego se revisa con los headers y las keys
#             new_like.publish()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 201, 'status_text':'Created successfully', 'message': message_serializer(message)},
#         json_dumps_params={'indent': 2})
#     return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'},
#                        json_dumps_params={'indent': 2})
#
#
# # requests.post(url, data={'message_id':3})
# def dislike_message(request):
#     if request.method == 'POST':
#         try:
#             message_id = request.POST.get('message_id')
#             results = Message.objects.filter(id=message_id)
#             message = results[0]
#             new_like = MessageDislike(message_id=message_id, user_id=1)
#             # Por mientras usuario 1, luego se revisa con los headers y las keys
#             new_like.publish()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 201, 'status_text':'Created successfully', 'message': message_serializer(message)},
#         json_dumps_params={'indent': 2})
#     return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'},
#                         json_dumps_params={'indent': 2})
#
#
# # requests.get(url, params={'message_id':1})
# # http://127.0.0.1:8000/message/reactions/?message_id=1
# def get_reactions(request):
#     try:
#         message_id = request.GET.get('message_id')
#         if 'limit' in request.GET:
#             limit = request.GET.get('limit')
#         else:
#             limit = 50
#         messages = Message.objects.filter(id=message_id)
#         message = messages[0]
#     except (IndexError, TypeError):
#         return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'},
#         json_dumps_params={'indent': 2})
#     return JsonResponse({'status_code': 200, 'status_text':'Ok',
#         'reactions': message_serializer(message, only_likes=True, limit=limit)},
#         json_dumps_params={'indent': 2})
#
#
# # requests.post(url, data={'group_id':1, 'text':'Estoy feliz #Happy #VivaLaVida'})
# def post_comment(request):
#     if request.method == 'POST':
#         try:
#             message_id = request.POST.get('message_id')
#             text = request.POST.get('text')
#             results = Message.objects.filter(id=message_id)
#             message = results[0]
#             new_comment = ThreadMessage(message_id=message_id, text=text, user_id=1)
#             # Por mientras usuario 1, luego se revisa con los headers y las keys
#             new_comment.publish()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 201, 'status_text':'Created successfully',
#             'message': message_serializer(message)}, json_dumps_params={'indent': 2})
#     elif request.method == 'PATCH':
#         try:
#             data = json.loads(request.body)
#             thread_id = data.get('thread_id')
#             new_text = data.get('text')
#             results = ThreadMessage.objects.filter(id=thread_id)
#             thread = results[0]
#             thread.text = new_text
#             thread.updated_at = datetime.datetime.now()
#             thread.publish()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object thread not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 201, 'status_text':'Updated successfully',
#             'thread': thread_serializer(thread)}, json_dumps_params={'indent': 2})
#     elif request.method == 'DELETE':
#         try:
#             data = json.loads(request.body)
#             thread_id = data.get('thread_id')
#             threads = ThreadMessage.objects.filter(id=thread_id)
#             thread = threads[0]
#             thread.delete()
#         except (IndexError, TypeError):
#             return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'},
#             json_dumps_params={'indent': 2})
#         return JsonResponse({'status_code': 200, 'status_text':'Deleted successfully'},
#             json_dumps_params={'indent': 2})
#     else:
#         return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'},
#                             json_dumps_params={'indent': 2})
#
#
# # # requests.get(url, params={'text': 'Comer'})
# # http://127.0.0.1:8000/search/hashtag/?text=Comer
# def search_hashtag(request):
#     try:
#         text = request.GET.get('text')
#         if 'limit' in request.GET:
#             limit = request.GET.get('limit')
#         else:
#             limit = 50
#         hashtags = Hashtag.objects.filter(hashtag_text=text)
#         hashtag = hashtags[0]
#         message_hashtags = MessageHashtag.objects.filter(hashtag_id=hashtag.id)
#         i = 0
#         messages = []
#         for mes_has in message_hashtags:
#             if i < limit:
#                 message = Message.objects.filter(id=mes_has.message_id)[0]
#                 messages.append(message_serializer(message))
#             i += 1
#
#     except (IndexError, TypeError):
#         return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'},
#         json_dumps_params={'indent': 2})
#     return JsonResponse({'status_code': 200, 'status_text':'Ok',
#         'messages': messages},
#         json_dumps_params={'indent': 2})
#
#
# # http://127.0.0.1:8000/search/username/?username=nachocontreras
# # # requests.get(url, params={'username': 'nachocontreras'})
# def search_username(request):
#     try:
#         username = request.GET.get('username')
#         if 'limit' in request.GET:
#             limit = request.GET.get('limit')
#         else:
#             limit = 50
#         users = User.objects.filter(username=username)
#         user = users[0]
#         messages_ = Message.objects.filter(user_id=user.id)
#         i = 0
#         messages = []
#         for message in messages_:
#             if i < limit:
#                 messages.append(message_serializer(message))
#             i += 1
#
#     except (IndexError, TypeError):
#         return JsonResponse({'status_code': 404, 'status_text': 'Object user not found.'},
#         json_dumps_params={'indent': 2})
#     return JsonResponse({'status_code': 200, 'status_text':'Ok',
#         'messages': messages},
#         json_dumps_params={'indent': 2})
