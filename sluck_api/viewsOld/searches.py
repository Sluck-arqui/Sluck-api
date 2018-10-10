from sluck_api.serializers import user_serializer, message_serializer, group_serializer
from django.http.response import JsonResponse
from sluck_api.models import Message, User, Group, MessageHashtag, Hashtag, \
                            MessageLike, MessageDislike, UserGroup


# # requests.get(url, params={'text': 'Comer'})
# http://127.0.0.1:8000/search/hashtag/?text=Comer
def search_hashtag(request):
    try:
        text = request.GET.get('text')
        if 'limit' in request.GET:
            limit = request.GET.get('limit')
        else:
            limit = 50
        hashtags = Hashtag.objects.filter(hashtag_text=text)
        hashtag = hashtags[0]
        message_hashtags = MessageHashtag.objects.filter(hashtag_id=hashtag.id)
        i = 0
        messages = []
        for mes_has in message_hashtags:
            if i < limit:
                message = Message.objects.filter(id=mes_has.message_id)[0]
                messages.append(message_serializer(message))
            i += 1

    except (IndexError, TypeError):
        return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
        json_dumps_params={'indent': 2})
    return JsonResponse({'status_code': 200, 'status_text':'Ok', 
        'messages': messages},
        json_dumps_params={'indent': 2})


# http://127.0.0.1:8000/search/username/?username=nachocontreras
# # requests.get(url, params={'username': 'nachocontreras'})
def search_username(request):
    try:
        username = request.GET.get('username')
        if 'limit' in request.GET:
            limit = request.GET.get('limit')
        else:
            limit = 50
        users = User.objects.filter(username=username)
        user = users[0]
        messages_ = Message.objects.filter(user_id=user.id)
        i = 0
        messages = []
        for message in messages_:
            if i < limit:
                messages.append(message_serializer(message))
            i += 1

    except (IndexError, TypeError):
        return JsonResponse({'status_code': 404, 'status_text': 'Object user not found.'}, 
        json_dumps_params={'indent': 2})
    return JsonResponse({'status_code': 200, 'status_text':'Ok', 
        'messages': messages},
        json_dumps_params={'indent': 2})