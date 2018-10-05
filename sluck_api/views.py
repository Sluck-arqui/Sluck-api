from sluck_api.serializers import user_serializer, message_serializer, group_serializer
from django.http.response import JsonResponse
from sluck_api.models import Message, User, Group


# Por ahora http://127.0.0.1:8000/user/?user_id=1
# requests.get(url, params={'user_id':1})
def get_user(request):
    try:
        user_id = request.GET.get('user_id')[0]
        users = User.objects.filter(id=user_id)
        user = users[0]
    except (IndexError, TypeError):
        return JsonResponse({'status_code': 404, 'status_text': 'Object user not found.'}, 
        json_dumps_params={'indent': 2})
    return JsonResponse({'status_code': 200, 'status_text':'Ok', 'user': user_serializer(user)},
        json_dumps_params={'indent': 2})

# Por ahora http://127.0.0.1:8000/message/?message_id=1
# requests.get(url, params={'message_id':1})
def get_message(request):
    try:
        message_id = request.GET.get('message_id')[0]
        messages = Message.objects.filter(id=message_id)
        message = messages[0]
    except (IndexError, TypeError):
        return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
        json_dumps_params={'indent': 2})
    return JsonResponse({'status_code': 200, 'status_text':'Ok', 'message': message_serializer(message)},
        json_dumps_params={'indent': 2})

# http://127.0.0.1:8000/group/?group_id=1
# requests.get(url, params={'group_id':1})
def get_group(request):
    try:
        group_id = request.GET.get('group_id')[0]
        groups = Group.objects.filter(id=group_id)
        group = groups[0]
    except (IndexError, TypeError):
        return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'}, 
        json_dumps_params={'indent': 2})
    return JsonResponse({'status_code': 200, 'status_text':'Ok', 'group': group_serializer(group)},
        json_dumps_params={'indent': 2})


def post_message(request):
    # No esta funcionando por errores de crsf
    if request.method == 'POST':
        try:
            group_id = request.POST.get('group_id')[0]
            text = request.POST.get('text')
            results = Group.objects.filter(id=group_id)
            group = results[0]
            new_message = Message(group_id=group_id, text=text, user_id=1) 
            # Por mientras usuario 1, luego se revisa con los headers y las keys
            new_message.publish()
            print(new_message, new_message.id)
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 201, 'status_text':'Created successfully', 'message': message_serializer(message)},
        json_dumps_params={'indent': 2})


def get_group_messages(request):
    try:
        group_id = request.GET.get('group_id')[0]
        results = Group.objects.filter(id=group_id)
        group = results[0]
        messages_ = Message.objects.filter(group_id=group_id)
        messages = []
        for message in messages_:
            messages.append(message_serializer(message))

    except (IndexError, TypeError):
        return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'}, 
        json_dumps_params={'indent': 2})
    return JsonResponse({'status_code': 200, 'status_text':'Ok', 'message': messages},
        json_dumps_params={'indent': 2})


def like_message(request):
    # No esta funcionando por errores de crsf
    if request.method == 'POST':
        try:
            message_id = request.POST.get('message_id')[0]
            results = Message.objects.filter(id=message_id)
            message = results[0]
            new_like = MessageLike(message_id=message_id, user_id=1) 
            # Por mientras usuario 1, luego se revisa con los headers y las keys
            new_like.publish()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 201, 'status_text':'Created successfully', 'message': message_serializer(message)},
        json_dumps_params={'indent': 2})


def dislike_message(request):
    # No esta funcionando por errores de crsf
    if request.method == 'POST':
        try:
            message_id = request.POST.get('message_id')[0]
            results = Message.objects.filter(id=message_id)
            message = results[0]
            new_like = MessageDisLike(message_id=message_id, user_id=1) 
            # Por mientras usuario 1, luego se revisa con los headers y las keys
            new_like.publish()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 201, 'status_text':'Created successfully', 'message': message_serializer(message)},
        json_dumps_params={'indent': 2})


def get_reactions(request):
    try:
        message_id = request.GET.get('message_id')[0]
        if 'limit' in request.GET:
            limit = request.GET.get('limit')
        else:
            limit = 50
        messages = Message.objects.filter(id=message_id)
        message = messages[0]
    except (IndexError, TypeError):
        return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
        json_dumps_params={'indent': 2})
    return JsonResponse({'status_code': 200, 'status_text':'Ok', 
        'reactions': message_serializer(message, only_likes=True, limit=limit)},
        json_dumps_params={'indent': 2})