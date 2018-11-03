from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    GroupSerializer,
    HashtagSerializer,
    MessageSerializer,
    MessageUpdateSerializer,
    MessageReactionsSerializer,
    ThreadMessageSerializer,
    ThreadMessageUpdateSerializer,
    ThreadMessageReactionsSerializer,
)
from .utils import (
    STATUS_CODE_200_DELETE,
    STATUS_CODE_400,
    STATUS_CODE_401,
    STATUS_CODE_403,
    STATUS_CODE_404,
    STATUS_CODE_405,
    STATUS_CODE_498,
    REACTION_TYPES,
)
from rest_framework import viewsets
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import (
    Message, User, Group,
    Hashtag, ThreadMessage,
    MessageReaction, ThreadMessageReaction,
)
import datetime
from rest_framework.authtoken.models import Token
from django.utils import timezone
import json
from django.db.models import Q


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
    API endpoint that allows hashtags to be viewed or edited.
    """
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = GroupSerializer


class ThreadMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows threads to be viewed or edited.
    """
    queryset = ThreadMessage.objects.all()
    serializer_class = UserSerializer


# User Views
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            instance, token = serializer.save()
            data = serializer.data
            data["oauth_token"] = str(token)
            keys = ['id', 'username', 'first_name', 'last_name', 'email', 'oauth_token', 'created_at', 'updated_at']
            data = {key: data[key] for key in keys}
            final_data = {'status_code': 201, 'user': data}
            return JsonResponse(final_data, status=201)
        return JsonResponse(STATUS_CODE_401, status=401)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        if data['username'] and data['password']:
            user = User.objects.filter(username=data['username'])
            if user:
                serializer = UserSerializer(user[0])
                if serializer.data['password'] == data['password']:
                    token = serializer.get_token()
                    data = serializer.data
                    if (timezone.now() - token.created).days <= 7:
                        data["oauth_token"] = str(token.key)

                    else:
                        token = serializer.new_token()
                        data["oauth_token"] = str(token.key)

                    keys = ['id', 'username', 'first_name', 'last_name', 'email', 'oauth_token', 'created_at', 'updated_at']
                    data = {key: data[key] for key in keys}
                    final_data = {'status_code': 201, 'user': data}
                    return JsonResponse(final_data, status=201)
                return JsonResponse({'status_text': 'Incorrect Password or Username'}, status=401)
            return JsonResponse({'status_text': 'Incorrect Password or Username'}, status=401)
        return JsonResponse(STATUS_CODE_400, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def get_user(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'GET':
                data = request.GET
                user_id = data.get('user_id', None)
                if user_id:
                    user = User.objects.filter(id=user_id)
                    if user:
                        serializer = UserSerializer(user[0])
                        return JsonResponse(serializer.data, safe=False, status=200)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            elif request.method == 'PATCH':
                data = JSONParser().parse(request)
                user_id = data.get('user_id', None)
                if user_id:
                    user = User.objects.filter(id=user_id)
                    if user:
                        serializer = UserUpdateSerializer(user[0], data)
                        if serializer.is_valid():
                            serializer.save()
                            return JsonResponse(
                                serializer.data, safe=False, status=200)
                        return JsonResponse(serializer.errors, status=400)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            elif request.method == 'DELETE':
                data = JSONParser().parse(request)
                user_id = data.get('user_id', None)
                if user_id:
                    user = User.objects.filter(id=user_id)
                    if user:
                        user[0].delete()
                        return JsonResponse(
                            STATUS_CODE_200_DELETE, status=200)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            else:
                return JsonResponse(STATUS_CODE_405, status=405)

        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)


# Group Views
@csrf_exempt
def get_group(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'GET':
                data = request.GET
                group_id = data.get('group_id', None)
                if group_id:
                    group = Group.objects.filter(id=group_id)
                    if group:
                        serializer = GroupSerializer(group[0])
                        return JsonResponse(serializer.data, safe=False, status=200)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            elif request.method == 'POST':
                data = JSONParser().parse(request)
                serializer = GroupSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=201)
                return JsonResponse(serializer.errors, status=400)

            elif request.method == 'PATCH':
                data = JSONParser().parse(request)
                group_id = data.get('group_id', None)
                if group_id:
                    group = Group.objects.filter(id=group_id)
                    if group:
                        serializer = GroupSerializer(group[0], data)
                        if serializer.is_valid():
                            serializer.save()
                            return JsonResponse(
                                serializer.data, safe=False, status=200)
                        return JsonResponse(serializer.errors, status=400)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            elif request.method == 'DELETE':
                data = JSONParser().parse(request)
                group_id = data.get('group_id', None)
                if group_id:
                    group = Group.objects.filter(id=group_id)
                    if group:
                        group[0].delete()
                        return JsonResponse(
                            STATUS_CODE_200_DELETE, status=200)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            else:
                return JsonResponse(STATUS_CODE_405, status=405)

        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)


@csrf_exempt
def new_group(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'POST':
                data = JSONParser().parse(request)
                serializer = GroupSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=201)
                return JsonResponse(serializer.errors, status=400)
            return JsonResponse(STATUS_CODE_405, status=405)

        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)


@csrf_exempt
def group_member(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'POST':
                data = JSONParser().parse(request)
                user_id = data.get('user_id', None)
                group_id = data.get('group_id', None)
                if user_id and group_id:
                    user = User.objects.filter(id=user_id)
                    group = Group.objects.filter(id=group_id)
                    if user and group:
                        group[0].members.add(user[0])
                        serializer = GroupSerializer(group[0])
                        return JsonResponse(serializer.data, status=201)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            elif request.method == 'DELETE':
                data = JSONParser().parse(request)
                user_id = data.get('user_id', None)
                group_id = data.get('group_id', None)
                if user_id and group_id:
                    user = User.objects.filter(id=user_id)
                    group = Group.objects.filter(id=group_id)
                    if user and group:
                        group[0].members.remove(user[0])
                        serializer = GroupSerializer(group[0])
                        return JsonResponse(
                            serializer.data, status=200)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            else:
                return JsonResponse(STATUS_CODE_405, status=405)

        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)


# Message Views
@csrf_exempt
def get_message(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'GET':
                data = request.GET
                message_id = data.get('message_id', None)
                if message_id:
                    message = Message.objects.filter(id=message_id)
                    if message:
                        serializer = MessageSerializer(message[0])
                        return JsonResponse(serializer.data, safe=False, status=200)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            elif request.method == 'PATCH':
                data = JSONParser().parse(request)
                message_id = data.get('message_id', None)
                if message_id:
                    message = Message.objects.filter(id=message_id)
                    if message:
                        serializer = MessageUpdateSerializer(message[0], data)
                        if serializer.is_valid():
                            serializer.save()
                            return JsonResponse(
                                serializer.data, safe=False, status=200)
                        return JsonResponse(serializer.errors, status=400)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            elif request.method == 'DELETE':
                data = JSONParser().parse(request)
                message_id = data.get('message_id', None)
                if message_id:
                    message = Message.objects.filter(id=message_id)
                    if message:
                        message[0].delete()
                        return JsonResponse(
                            STATUS_CODE_200_DELETE, status=200)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            else:
                return JsonResponse(STATUS_CODE_405, status=405)

        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)


@csrf_exempt
def post_message(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'POST':
                data = JSONParser().parse(request)
                user_id = token.user_id
                group_id = data.get('group_id', None)
                text = data.get('text', None)
                if user_id and group_id and text:
                    user = User.objects.filter(id=user_id)
                    group = Group.objects.filter(id=group_id)
                    if user and group:
                        message = Message(
                            author=user[0],
                            group=group[0],
                            text=text,
                        ).publish()
                        serializer = MessageSerializer(message)
                        return JsonResponse(serializer.data, status=201)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)
            return JsonResponse(STATUS_CODE_405, status=405)

        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)


@csrf_exempt
def chat(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'GET':
                data = request.GET
                user1 = data.get('user1', None)
                user2 = data.get('user2', None)
                if user1 and user2:
                    groups1 = User.objects.filter(id=user1)[0].groups
                    groups2 = User.objects.filter(id=user2)[0].groups
                    groups = list(set(groups1) & set(groups2))
                    messages = Message.objects.filter(group__in=groups)
                    if messages:
                        information = {'messages': []}
                        for message in messages:
                            serializer = MessageReactionsSerializer(message)
                            information['messages'].append(serializer.data)
                        return JsonResponse(information, safe=False, status=200)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)
            return JsonResponse(STATUS_CODE_405, status=405)

        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)


@csrf_exempt
def message_reactions(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'GET':
                data = request.GET
                message_id = data.get('message_id', None)
                limit = data.get('limit', 50)
                if message_id:
                    message = Message.objects.filter(id=message_id)
                    if message:
                        serializer = MessageReactionsSerializer(message[0])
                        return JsonResponse(serializer.data, safe=False, status=200)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)
            elif request.method == 'POST':
                data = JSONParser().parse(request)
                user_id = token.user_id
                message_id = data.get('message_id', None)
                react_type = data.get('reaction_type', None)
                if user_id and message_id and react_type:
                    user = User.objects.filter(id=user_id)
                    message = Message.objects.filter(id=message_id)
                    if user and message and react_type in REACTION_TYPES.keys():
                        if user[0] in message[0].reactions.all():
                            return JsonResponse(STATUS_CODE_403, status=403)
                        if user[0] not in message[0].reactions.all():
                            react = MessageReaction(author=user[0],
                                                    message=message[0],
                                                    reaction_type=react_type)
                            react.publish()
                            serializer = MessageSerializer(message[0])
                            return JsonResponse(serializer.data, status=201)
                    elif user and message and react_type == -1:
                        if user[0] in message[0].reactions.all():
                            reaction = MessageReaction.objects.filter(author=user[0])
                            if reaction:
                                reaction.delete()
                                serializer = MessageSerializer(message[0])
                                return JsonResponse(serializer.data, status=200)
                            else:
                                return JsonResponse(
                                        STATUS_CODE_400, status=400)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)
            return JsonResponse(STATUS_CODE_405, status=405)

        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)


@csrf_exempt
def post_comment(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'POST':
                data = JSONParser().parse(request)
                user_id = token.user_id
                message_id = data.get('message_id', None)
                text = data.get('text', None)
                if user_id and message_id and text:
                    user = User.objects.filter(id=user_id)
                    message = Message.objects.filter(id=message_id)
                    if user and message:
                        thread = ThreadMessage(
                            author=user[0],
                            message=message[0],
                            text=text,
                        ).publish()
                        serializer = ThreadMessageSerializer(thread)
                        return JsonResponse(serializer.data, status=201)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            elif request.method == 'PATCH':
                data = JSONParser().parse(request)
                thread_id = data.get('thread_id', None)
                if thread_id:
                    thread = ThreadMessage.objects.filter(id=thread_id)
                    if thread:
                        serializer = ThreadMessageUpdateSerializer(thread[0], data)
                        if serializer.is_valid():
                            serializer.save()
                            return JsonResponse(
                                serializer.data, safe=False, status=200)
                        return JsonResponse(serializer.errors, status=400)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            elif request.method == 'DELETE':
                data = JSONParser().parse(request)
                thread_id = data.get('thread_id', None)
                if thread_id:
                    thread = ThreadMessage.objects.filter(id=thread_id)
                    if thread:
                        thread[0].delete()
                        return JsonResponse(
                            STATUS_CODE_200_DELETE, status=200)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)

            else:
                return JsonResponse(STATUS_CODE_405, status=405)

        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)


@csrf_exempt
def thread_reactions(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'GET':
                data = request.GET
                thread_id = data.get('thread_id', None)
                limit = data.get('limit', 50)
                if thread_id:
                    thread = ThreadMessage.objects.filter(id=thread_id)
                    if thread:
                        serializer = ThreadMessageReactionsSerializer(thread[0])
                        return JsonResponse(serializer.data, safe=False, status=200)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)
            elif request.method == 'POST':
                data = JSONParser().parse(request)
                user_id = token.user_id
                thread_id = data.get('thread_id', None)
                react_type = data.get('reaction_type', None)
                if user_id and thread_id and react_type:
                    user = User.objects.filter(id=user_id)
                    thread = ThreadMessage.objects.filter(id=thread_id)
                    if user and thread and react_type in REACTION_TYPES.keys():
                        if user[0] in thread[0].reactions.all():
                            return JsonResponse(STATUS_CODE_403, status=403)
                        if user[0] not in thread[0].reactions.all():
                            react = ThreadMessageReaction(author=user[0],
                                                          thread=thread[0],
                                                          reaction_type=react_type)
                            react.publish()
                            serializer = ThreadMessageSerializer(thread[0])
                            return JsonResponse(serializer.data, status=201)
                    elif user and thread_id and react_type == -1:
                        if user[0] in thread[0].reactions.all():
                            reaction = ThreadMessageReaction.objects.filter(author=user[0])
                            if reaction:
                                reaction.delete()
                                serializer = ThreadMessageSerializer(thread[0])
                                return JsonResponse(serializer.data, status=200)
                            else:
                                return JsonResponse(
                                        STATUS_CODE_400, status=400)
                    return JsonResponse(
                        STATUS_CODE_404, status=404)
                return JsonResponse(
                    STATUS_CODE_400, status=400)
            return JsonResponse(STATUS_CODE_405, status=405)
        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)


@csrf_exempt
def search_hashtag(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'GET':
                data = request.GET
                hashtag_text = data.get('text', None)
                limit = data.get('limit', 50)
                if hashtag_text:
                    hashtag = Hashtag.objects.filter(text=hashtag_text)
                    messages = Message.objects.filter(hashtags__text=hashtag_text)
                    if messages:
                        serializer = MessageSerializer(messages, many=True)
                        return JsonResponse(serializer.data, safe=False, status=200)
                    return JsonResponse([], safe=False, status=200)
                return JsonResponse(
                    STATUS_CODE_400, status=400)
            return JsonResponse(STATUS_CODE_405, status=405)

        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)


@csrf_exempt
def search_username(request):
    try:
        token = Token.objects.get(key=request.META['HTTP_OAUTH_TOKEN'])
        if (timezone.now() - token.created).days <= 7:
            if request.method == 'GET':
                data = request.GET
                username = data.get('username', None)
                limit = data.get('limit', 50)
                if username:
                    user = User.objects.filter(username=username)
                    if user:
                        messages = user[0].messages.all()
                        serializer = MessageSerializer(messages, many=True)
                        return JsonResponse(serializer.data, safe=False, status=200)
                    return JsonResponse([], safe=False, status=200)
                return JsonResponse(
                    STATUS_CODE_400, status=400)
            return JsonResponse(STATUS_CODE_405, status=405)

        else:
            return JsonResponse(STATUS_CODE_498, status=498)

    except KeyError:
        return JsonResponse(STATUS_CODE_498, status=498)

    except Token.DoesNotExist:
        return JsonResponse(STATUS_CODE_498, status=498)
