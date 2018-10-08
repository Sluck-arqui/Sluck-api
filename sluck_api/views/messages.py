from sluck_api.serializers import user_serializer, message_serializer, group_serializer, thread_serializer
from django.http.response import JsonResponse
from sluck_api.models import Message, User, Group, MessageHashtag, Hashtag, \
                            MessageLike, MessageDislike, UserGroup, ThreadMessage, \
                            ThreadLike, ThreadDislike
import datetime


# Por ahora http://127.0.0.1:8000/message/?message_id=1
# requests.get(url, params={'message_id':1})
def get_message(request):
    if request.method == 'GET':
        try:
            message_id = request.GET.get('message_id')
            messages = Message.objects.filter(id=message_id)
            message = messages[0]
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 200, 'status_text':'Ok', 'message': message_serializer(message)},
            json_dumps_params={'indent': 2})
    elif request.method == 'DELETE':
        # requests.delete(url, params={'message_id':5})
        try:
            message_id = request.GET.get('message_id')
            messages = Message.objects.filter(id=message_id)
            message = messages[0]
            message.delete()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 200, 'status_text':'Deleted successfully'},
            json_dumps_params={'indent': 2})
    elif request.method == 'PATCH':
        try:
            message_id = request.GET.get('message_id')
            new_text = request.GET.get('text')
            results = Message.objects.filter(id=message_id)
            message = results[0]
            message.text = new_text
            message.updated_at = datetime.datetime.now()     
            message.publish(edit=True)
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 201, 'status_text':'Updated successfully', 
            'message': message_serializer(message)}, json_dumps_params={'indent': 2})
    else:
        return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'}, 
                            json_dumps_params={'indent': 2})


# requests.post(url, params={'group_id':1, 'text':'Estoy feliz #Happy #VivaLaVida'})
def post_message(request):
    if request.method == 'POST':
        try:
            group_id = request.GET.get('group_id')
            text = request.GET.get('text')
            results = Group.objects.filter(id=group_id)
            group = results[0]
            new_message = Message(group_id=group_id, text=text, user_id=2) 
            # Por mientras usuario 1, luego se revisa con los headers y las keys
            new_message.publish()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 201, 'status_text':'Created successfully', 
            'message': message_serializer(new_message)}, json_dumps_params={'indent': 2})
    elif request.method == 'GET':
        try:
            group_id = request.GET.get('group_id')
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
    else:
        return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'}, 
                            json_dumps_params={'indent': 2})


# requests.post(url, params={'message_id':3})
def like_message(request):
    if request.method == 'POST':
        try:
            message_id = request.GET.get('message_id')
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
    return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'}, 
                       json_dumps_params={'indent': 2})


# requests.post(url, params={'message_id':3})
def dislike_message(request):
    if request.method == 'POST':
        try:
            message_id = request.GET.get('message_id')
            results = Message.objects.filter(id=message_id)
            message = results[0]
            new_like = MessageDislike(message_id=message_id, user_id=1) 
            # Por mientras usuario 1, luego se revisa con los headers y las keys
            new_like.publish()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 201, 'status_text':'Created successfully', 'message': message_serializer(message)},
        json_dumps_params={'indent': 2})
    return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'}, 
                        json_dumps_params={'indent': 2})


# requests.get(url, params={'message_id':1})
# http://127.0.0.1:8000/message/reactions/?message_id=1
def get_reactions(request):
    try:
        message_id = request.GET.get('message_id')
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


# requests.post(url, params={'group_id':1, 'text':'Estoy feliz #Happy #VivaLaVida'})
def post_comment(request):
    if request.method == 'POST':
        try:
            message_id = request.GET.get('message_id')
            text = request.GET.get('text')
            results = Message.objects.filter(id=message_id)
            message = results[0]
            new_comment = ThreadMessage(message_id=message_id, text=text, user_id=1) 
            # Por mientras usuario 1, luego se revisa con los headers y las keys
            new_comment.publish()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 201, 'status_text':'Created successfully', 
            'message': message_serializer(message)}, json_dumps_params={'indent': 2})
    elif request.method == 'PATCH':
        try:
            thread_id = request.GET.get('thread_id')
            new_text = request.GET.get('text')
            results = ThreadMessage.objects.filter(id=thread_id)
            thread = results[0]
            thread.text = new_text
            thread.updated_at = datetime.datetime.now()     
            thread.publish()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object thread not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 201, 'status_text':'Updated successfully', 
            'thread': thread_serializer(thread)}, json_dumps_params={'indent': 2})
    elif request.method == 'DELETE':
        try:
            thread_id = request.GET.get('thread_id')
            threads = ThreadMessage.objects.filter(id=thread_id)
            thread = threads[0]
            thread.delete()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 200, 'status_text':'Deleted successfully'},
            json_dumps_params={'indent': 2})
    else:
        return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'}, 
                            json_dumps_params={'indent': 2})
