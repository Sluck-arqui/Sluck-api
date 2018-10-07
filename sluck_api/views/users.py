from sluck_api.serializers import user_serializer, message_serializer, group_serializer
from django.http.response import JsonResponse
from sluck_api.models import Message, User, Group, MessageHashtag, Hashtag, \
                            MessageLike, MessageDislike, UserGroup


# Por ahora http://127.0.0.1:8000/user/?user_id=1
# requests.get(url, params={'user_id':1})
def get_user(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')[0]
            users = User.objects.filter(id=user_id)
            user = users[0]
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object user not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 200, 'status_text':'Ok', 'user': user_serializer(user)},
            json_dumps_params={'indent': 2})
    elif request.method == 'DELETE':
        try:
            user_id = request.GET.get('user_id')[0]
            users = User.objects.filter(id=user_id)
            user = users[0]
            user.delete()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object user not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 200, 'status_text':'Deleted successfully'},
            json_dumps_params={'indent': 2})
    else:
        return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'}, 
                            json_dumps_params={'indent': 2})