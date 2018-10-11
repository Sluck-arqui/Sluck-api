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
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=401)
    else:
        return JsonResponse({'status_text': 'Unauthorized'}, status=401)


@csrf_exempt
def get_user(request):
    if request.method == 'GET':
        data = request.GET
        user_id = data.get('user_id', None)
        if user_id:
            user = User.objects.filter(id=user_id)
            if user:
                serializer = UserSerializer(user[0])
                return JsonResponse(serializer.data, safe=False, status=200)
        return JsonResponse(
            {'status_text': 'Object user not found'}, status=404)

    elif request.method == 'PATCH' and request.body:
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        if user_id:
            user = User.objects.filter(id=user_id)
            if user:
                serializer = UserSerializer(user[0], data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(
                        serializer.data, safe=False, status=200)
        return JsonResponse(
            {'status_text': 'Object user not found'}, status=404)

    elif request.method == 'DELETE' and request.body:
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        if user_id:
            user = User.objects.filter(id=user_id)
            if user:
                user[0].delete()
                return JsonResponse(
                    {'status_text': 'Deleted successfully'}, status=200)
        return JsonResponse(
            {'status_text': 'Object user not found'}, status=404)

    else:
        return JsonResponse({'status_text': 'Unauthorized'}, status=401)
