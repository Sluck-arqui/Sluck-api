from sluck_api.serializers import user_serializer, message_serializer, group_serializer
from django.http.response import JsonResponse
from sluck_api.models import Message, User, Group, MessageHashtag, Hashtag, \
                            MessageLike, MessageDislike, UserGroup


# http://127.0.0.1:8000/group/?group_id=1
# requests.get(url, params={'group_id':1})
def get_group(request):
    if request.method == 'GET':
        try:
            group_id = request.GET.get('group_id')
            groups = Group.objects.filter(id=group_id)
            group = groups[0]
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 200, 'status_text':'Ok', 'group': group_serializer(group)},
            json_dumps_params={'indent': 2})
    elif request.method == 'DELETE':
        try:
            group_id = request.GET.get('group_id')
            groups = Group.objects.filter(id=group_id)
            group = groups[0]
            group.delete()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 200, 'status_text':'Deleted successfully'},
            json_dumps_params={'indent': 2})
    else:
        return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'}, 
                            json_dumps_params={'indent': 2})


# requests.post(url, params={'name':'Second group', 'description':'This is the second group'})
def new_group(request):
    if request.method == 'POST':
        try:
            name = request.GET.get('name')
            description = request.GET.get('description')
            group = Group(name=name, description=description)
            group.publish()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 400, 'status_text': 'Bad request.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 201, 'status_text':'Created successfully', 
            'group': group_serializer(group)}, json_dumps_params={'indent': 2})
    else:
        return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'}, 
                            json_dumps_params={'indent': 2})


# requests.post(url, params={'group_id':3, 'user_id':1})
def group_member(request):
    if request.method == 'POST':
        try:
            group_id = request.GET.get('group_id')
            user_id = request.GET.get('user_id')
            groups = Group.objects.filter(id=group_id)
            group = groups[0]
            new_member = UserGroup(user_id=user_id, group_id=group_id)
            new_member.publish()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object group not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 200, 'status_text':'Added successfully', 
            'group': group_serializer(group)}, json_dumps_params={'indent': 2})
    elif request.method == 'DELETE':
        # requests.delete(url, params={'group_id':3, 'user_id':1})
        try:
            group_id = request.GET.get('group_id')
            user_id = request.GET.get('user_id')
            groups = Group.objects.filter(id=group_id)
            group = groups[0]
            new_member = UserGroup.objects.filter(user_id=user_id, group_id=group_id)
            new_member.delete()
        except (IndexError, TypeError):
            return JsonResponse({'status_code': 404, 'status_text': 'Object group or user not found.'}, 
            json_dumps_params={'indent': 2})
        return JsonResponse({'status_code': 200, 'status_text':'Deleted successfully'}, 
                            json_dumps_params={'indent': 2})
    else:
        return JsonResponse({'status_code': 405, 'status_text': 'Method not allowed.'}, 
                            json_dumps_params={'indent': 2})
