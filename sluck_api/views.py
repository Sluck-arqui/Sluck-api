from sluck_api.serializers import user_serializer, message_serializer
from django.http.response import JsonResponse
from sluck_api.models import Message, User


# Por ahora http://127.0.0.1:8000/user/?user_id=1
def get_user(request):
    try:
        user_id = request.GET.get('user_id')
        users = User.objects.filter(id=user_id)
        user = users[0]
    except IndexError:
        return JsonResponse({'status_code': 404, 'status_text': 'Object user not found.'}, 
        json_dumps_params={'indent': 2})
    return JsonResponse({'status_code': 200, 'status_text':'Ok', 'user': user_serializer(user)},
        json_dumps_params={'indent': 2})

# Por ahora http://127.0.0.1:8000/message/?message_id=1
def get_message(request):
    try:
        message_id = request.GET.get('message_id')
        messages = Message.objects.filter(id=message_id)
        message = messages[0]
    except IndexError:
        return JsonResponse({'status_code': 404, 'status_text': 'Object message not found.'}, 
        json_dumps_params={'indent': 2})
    return JsonResponse({'status_code': 200, 'status_text':'Ok', 'message': message_serializer(message)},
        json_dumps_params={'indent': 2})