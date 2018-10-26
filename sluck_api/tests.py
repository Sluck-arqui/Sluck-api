from django.test import TestCase
from rest_framework.test import APIRequestFactory
import sluck_api.views as views
from unittest import skip, skipIf
import json
from rest_framework.authtoken.models import Token
from .models import (
    User,
    Group,
    Hashtag,
    Message,
    ThreadMessage,
)
from .serializers import (
    UserSerializer,
    GroupSerializer,
    HashtagSerializer,
    MessageSerializer,
    MessageReactionsSerializer,
    ThreadMessageSerializer,
    ThreadMessageReactionsSerializer,
)
from .utils import (
    STATUS_CODE_200_DELETE,
    STATUS_CODE_400,
    STATUS_CODE_403,
    STATUS_CODE_404,
    STATUS_CODE_405,
)


class SessionTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_valid_can_register(self):
        view = views.register
        data = {
            'username': 'nachocontreras',
            'first_name': 'Ignacio',
            'last_name': 'Contreras',
            'email': 'mimail@uc.cl',
            'password': 'password',
        }
        request = self.factory.post('/register/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        created_user = UserSerializer(
            User.objects.get(id=parsed_response['user']['id'])).data
        for key in list(data.keys())[:-1]:
            self.assertEqual(data[key], parsed_response['user'][key])
            self.assertEqual(data[key], created_user[key])

    def test_invalid_cant_register(self):
        view = views.register
        data = {
            'username': 'nachocontreras',
            'first_name': 'Ignacio',
            'email': 'mimail@uc.cl',
            'password': 'password',
        }
        request = self.factory.post('/register/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 400)

    def test_get_is_not_allowed(self):
        view = views.register
        request = self.factory.get('/register/')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = STATUS_CODE_405
        self.assertEqual(response.status_code, 405)
        self.assertEqual(parsed_response, expected_response)


class UserTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username='nachocontreras',
            first_name='Ignacio',
            last_name='Contreras',
            email='mimail@uc.cl',
            password='password',
        )
        self.token = Token.objects.create(user=self.user)

    def test_get_user(self):
        view = views.get_user
        data = {'user_id': self.user.id}
        request = self.factory.get('/user/', data, format='json', HTTP_OAUTH_TOKEN=self.token)
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = {
            'id': self.user.id,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'password': self.user.password,
        }

        self.assertEqual(response.status_code, 200)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

    def test_update_user(self):
        view = views.get_user
        data = {
            'user_id': self.user.id,
            'username': 'raiperez',
            'first_name': 'raimundo',
            'last_name': 'perez',
            'email': 'nuevomail@mail.com',
            'password': 'contraseñanueva',
        }
        request = self.factory.patch('/user/', data, format='json', HTTP_OAUTH_TOKEN=self.token)
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = {
            'id': self.user.id,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': 'nuevomail@mail.com',
            'password': 'contraseñanueva',
        }
        self.assertEqual(response.status_code, 200)

        updated_user = UserSerializer(
            User.objects.get(id=self.user.id)).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])
            self.assertEqual(parsed_response[key], updated_user[key])

    def test_delete_user(self):
        view = views.get_user
        data = {'user_id': self.user.id}
        request = self.factory.delete('/user/', data, format='json', HTTP_OAUTH_TOKEN=self.token)
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = STATUS_CODE_200_DELETE

        self.assertEqual(response.status_code, 200)
        self.assertEqual(parsed_response, expected_response)
        with self.assertRaises(User.DoesNotExist):
            deleted_user = User.objects.get(id=self.user.id)

    def test_user_not_found(self):
        view = views.get_user
        data = {'user_id': 50}

        expected_response = STATUS_CODE_404

        # GET
        request = self.factory.get('/user/', data, format='json', HTTP_OAUTH_TOKEN=self.token)
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

        # PATCH
        request = self.factory.patch('/user/', data, format='json', HTTP_OAUTH_TOKEN=self.token)
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

        # DELETE
        request = self.factory.delete('/user/', data, format='json', HTTP_OAUTH_TOKEN=self.token)
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

    def test_post_is_not_allowed(self):
        view = views.get_user
        data = {
            'username': 'nachocontreras',
            'first_name': 'Ignacio',
            'last_name': 'Contreras',
            'email': 'mimail@uc.cl',
            'password': 'password',
        }
        request = self.factory.post('/user/', data, format='json', HTTP_OAUTH_TOKEN=self.token)
        response = view(request)
        parsed_response = json.loads(response.content)
        expected_response = STATUS_CODE_405
        self.assertEqual(response.status_code, 405)
        self.assertEqual(parsed_response, expected_response)


class GroupTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.group = Group.objects.create(
            name='cabros',
            description='Grupo de cabros'
        )
        self.user1 = User.objects.create(
            username='nachocontreras',
            first_name='Ignacio',
            last_name='Contreras',
            email='mimail@uc.cl',
            password='password',
        )
        self.user2 = User.objects.create(
            username='raiperez',
            first_name='Raimundo',
            last_name='Perez',
            email='mimail2@uc.cl',
            password='password',
        )

    def test_create_group(self):
        view = views.new_group
        data = {
            'name': 'otros cabros',
            'description': 'Grupo de otros cabros tela',
        }
        request = self.factory.post('/group/new/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        self.assertEqual(response.status_code, 201)

        created_group = GroupSerializer(
            Group.objects.get(id=parsed_response['id'])).data
        for key in data:
            self.assertEqual(data[key], parsed_response[key])
            self.assertEqual(data[key], created_group[key])

    def test_get_group(self):
        view = views.get_group
        data = {'group_id': self.group.id}
        request = self.factory.get('/group/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = {
            'id': self.group.id,
            'name': 'cabros',
            'members': [],
            'description': 'Grupo de cabros',
        }

        self.assertEqual(response.status_code, 200)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

    def test_update_group(self):
        view = views.get_group
        data = {
            'group_id': self.group.id,
            'name': 'alumnosdcc',
            'description': 'Grupo de alumnos del dcc',
        }
        request = self.factory.patch('/group/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = {
            'id': self.group.id,
            'name': 'alumnosdcc',
            'description': 'Grupo de alumnos del dcc',
        }
        self.assertEqual(response.status_code, 200)

        updated_group = GroupSerializer(
            Group.objects.get(id=self.group.id)).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])
            self.assertEqual(parsed_response[key], updated_group[key])

    def test_delete_group(self):
        view = views.get_group
        data = {'group_id': self.group.id}
        request = self.factory.delete('/group/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = STATUS_CODE_200_DELETE

        self.assertEqual(response.status_code, 200)
        self.assertEqual(parsed_response, expected_response)
        with self.assertRaises(Group.DoesNotExist):
            deleted_group = Group.objects.get(id=self.group.id)

    def test_group_not_found(self):
        view = views.get_group
        data = {'group_id': 50}

        expected_response = STATUS_CODE_404

        # GET
        request = self.factory.get('/group/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

        # PATCH
        request = self.factory.patch('/group/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

        # DELETE
        request = self.factory.delete('/group/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

    def test_post_is_not_allowed(self):
        view = views.get_group
        data = {
            'name': 'cabros',
            'description': 'Grupo de cabros',
        }
        request = self.factory.post('/group/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        expected_response = STATUS_CODE_405
        self.assertEqual(response.status_code, 405)
        self.assertEqual(parsed_response, expected_response)

    def test_group_member(self):
        view = views.group_member

        # Add first member
        data = {'group_id': self.group.id, 'user_id': self.user1.id}
        expected_response = {
            'id': self.group.id,
            'members': [
                {'id': 1, 'username': 'nachocontreras'},
            ],
            'description': self.group.description,
            'name': self.group.name,
        }
        request = self.factory.post('/group/member/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        # Check response
        self.assertEqual(response.status_code, 201)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

        # Check DB
        parsed_response = GroupSerializer(
            Group.objects.get(id=self.group.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

        # Add second member
        data = {'group_id': self.group.id, 'user_id': self.user2.id}
        expected_response = {
            'id': self.group.id,
            'members': [
                {'id': 1, 'username': 'nachocontreras'},
                {'id': 2, 'username': 'raiperez'},
            ],
            'description': self.group.description,
            'name': self.group.name,
        }
        request = self.factory.post('/group/member/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        # Check response
        self.assertEqual(response.status_code, 201)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

        # Check DB
        parsed_response = GroupSerializer(
            Group.objects.get(id=self.group.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

        # Delete first user
        data = {'group_id': self.group.id, 'user_id': self.user1.id}
        expected_response = {
            'id': self.group.id,
            'members': [
                {'id': 2, 'username': 'raiperez'},
            ],
            'description': self.group.description,
            'name': self.group.name,
        }
        request = self.factory.delete('/group/member/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        # Check response
        self.assertEqual(response.status_code, 200)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

        # Check DB
        parsed_response = GroupSerializer(
            Group.objects.get(id=self.group.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])


class MessageTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.group = Group.objects.create(
            name='cabros',
            description='Grupo de cabros'
        )
        self.user = User.objects.create(
            username='raiperez',
            first_name='Raimundo',
            last_name='Perez',
            email='mimail2@uc.cl',
            password='password',
        )
        self.message = Message(
            text='Mensaje woohoo #wena!  @raiperez jeje @hola',
            author=self.user,
            group=self.group,
        ).publish()
        self.liked_message = Message(
            text='Este mensaje sera likeado',
            author=self.user,
            group=self.group,
        ).publish()
        # self.liked_message.likers.add(self.user)

    def test_create_message(self):
        view = views.post_message
        data = {
            'user_id': self.user.id,
            'group_id': self.group.id,
            'text': 'Otro comentairio de #ejemplo',
        }
        request = self.factory.post('/message/new/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        expected_response = {
            'author': self.user.id,
            'group': self.group.id,
            'text': 'Otro comentairio de #ejemplo',
            'likes': 0,
            'dislikes': 0,
            'hashtags': [
                {'id': 2, 'text': 'ejemplo'},
            ],
            'mentions': [],
            'likers': [],
            'dislikers': [],
            'threads': [],
        }

        self.assertEqual(response.status_code, 201)
        created_message = MessageSerializer(
            Message.objects.get(id=parsed_response['id'])).data
        for key in expected_response:
            self.assertEqual(expected_response[key], parsed_response[key])
            self.assertEqual(expected_response[key], created_message[key])

    def test_get_message(self):
        view = views.get_message
        data = {'message_id': self.message.id}
        request = self.factory.get('/message/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = {
            'id': self.message.id,
            'author': self.user.id,
            'group': self.group.id,
            'text': self.message.text,
            'likes': self.message.likes,
            'dislikes': self.message.dislikes,
            'hashtags': [
                {'id': 1, 'text': 'wena!'},
            ],
            'mentions': [
                {'id': self.user.id, 'username': self.user.username},
            ],
            'likers': [],
            'dislikers': [],
            'threads': [],
        }
        self.assertEqual(response.status_code, 200)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

    def test_update_message(self):
        view = views.get_message
        data = {
            'message_id': self.message.id,
            'text': 'mensaje editado!',
        }
        request = self.factory.patch('/message/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        expected_response = {
            'id': self.message.id,
            'author': self.user.id,
            'group': self.group.id,
            'text': 'mensaje editado!',
            'likes': self.message.likes,
            'dislikes': self.message.dislikes,
            'hashtags': [],
            'mentions': [],
            'likers': [],
            'dislikers': [],
            'threads': [],
        }
        self.assertEqual(response.status_code, 200)
        updated_message = MessageSerializer(
            Message.objects.get(id=self.message.id)).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])
            self.assertEqual(parsed_response[key], updated_message[key])

    def test_delete_message(self):
        view = views.get_message
        data = {'message_id': self.message.id}
        request = self.factory.delete('/message/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = STATUS_CODE_200_DELETE

        self.assertEqual(response.status_code, 200)
        self.assertEqual(parsed_response, expected_response)
        with self.assertRaises(Message.DoesNotExist):
            deleted_message = Message.objects.get(id=self.message.id)

    def test_message_not_found(self):
        view = views.get_message
        data = {'message_id': 50}

        expected_response = STATUS_CODE_404

        # GET
        request = self.factory.get('/message/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

        # PATCH
        request = self.factory.patch('/message/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

        # DELETE
        request = self.factory.delete('/message/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

    def test_post_is_not_allowed(self):
        view = views.get_message
        data = {
            'user_id': self.user.id,
            'group_id': self.group.id,
            'text': 'Otro comentairio de #ejemplo',
        }
        request = self.factory.post('/message/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        expected_response = STATUS_CODE_405
        self.assertEqual(response.status_code, 405)
        self.assertEqual(parsed_response, expected_response)

    def test_react_to_message(self):
        reaction_view = views.message_reactions

        # Like
        data = {'message_id': self.message.id, 'user_id': self.user.id,
                'reaction_type': 1}
        expected_response = {
            'id': self.message.id,
            'author': self.user.id,
            'group': self.group.id,
            'text': self.message.text,
            'likes': 1,
            'dislikes': 0,
            'hashtags': [
                {'id': 1, 'text': 'wena!'},
            ],
            'mentions': [
                {'id': self.user.id, 'username': self.user.username},
            ],
            'likers': [
                {'id': self.user.id, 'username': self.user.username},
            ],
            'dislikers': [],
            'threads': [],
        }
        request = self.factory.post('/message/like/', data, format='json')
        response = reaction_view(request)
        parsed_response = json.loads(response.content)

        # Check response and DB Data
        self.assertEqual(response.status_code, 201)
        db_data = MessageSerializer(
            Message.objects.get(id=self.message.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])
            self.assertEqual(db_data[key], expected_response[key])
        # Can't Dislike
        data = {'message_id': self.message.id, 'user_id': self.user.id}
        request = self.factory.post('/message/dislike/', data, format='json')
        response = reaction_view(request)
        parsed_response = json.loads(response.content)
        expected_response = STATUS_CODE_403
        self.assertEqual(response.status_code, 403)
        self.assertEqual(parsed_response, expected_response)
        # Unlike
        data = {'message_id': self.message.id, 'user_id': self.user.id}
        expected_response = {
            'id': self.message.id,
            'author': self.user.id,
            'group': self.group.id,
            'text': self.message.text,
            'likes': 0,
            'dislikes': 0,
            'hashtags': [
                {'id': 1, 'text': 'wena!'},
            ],
            'mentions': [
                {'id': self.user.id, 'username': self.user.username},
            ],
            'likers': [],
            'dislikers': [],
            'threads': [],
        }
        request = self.factory.post('/message/like/', data, format='json')
        response = reaction_view(request)
        parsed_response = json.loads(response.content)

        # Check response and DB Data
        self.assertEqual(response.status_code, 201)
        db_data = MessageSerializer(
            Message.objects.get(id=self.message.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])
            self.assertEqual(db_data[key], expected_response[key])
        # Dislike
        data = {'message_id': self.message.id, 'user_id': self.user.id,
                'reaction_type': 2}
        expected_response = {
            'id': self.message.id,
            'author': self.user.id,
            'group': self.group.id,
            'text': self.message.text,
            'likes': 0,
            'dislikes': 1,
            'hashtags': [
                {'id': 1, 'text': 'wena!'},
            ],
            'mentions': [
                {'id': self.user.id, 'username': self.user.username},
            ],
            'likers': [],
            'dislikers': [
                {'id': self.user.id, 'username': self.user.username},
            ],
            'threads': [],
        }
        request = self.factory.post('/message/dislike/', data, format='json')
        response = reaction_view(request)
        parsed_response = json.loads(response.content)

        # Check response and DB Data
        self.assertEqual(response.status_code, 201)
        db_data = MessageSerializer(
            Message.objects.get(id=self.message.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])
            self.assertEqual(db_data[key], expected_response[key])

    def test_get_message_reactions(self):
        view = views.message_reactions
        data = {'message_id': self.liked_message.id}
        request = self.factory.get('/message/reactions', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = {
            'id': self.liked_message.id,
            'likes': 1,
            'dislikes': 0,
            'likers': [
                {'id': self.user.id, 'username': self.user.username},
            ],
            'dislikers': [],
        }

        self.assertEqual(response.status_code, 200)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])


class ThreadMessageTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.group = Group.objects.create(
            name='cabros',
            description='Grupo de cabros'
        )
        self.user = User.objects.create(
            username='raiperez',
            first_name='Raimundo',
            last_name='Perez',
            email='mimail2@uc.cl',
            password='password',
        )
        self.user2 = User.objects.create(
            username='nachocontreras',
            first_name='Ignacio',
            last_name='Contreras',
            email='mimail@uc.cl',
            password='password',
        )
        self.message = Message(
            text='Mensaje con muchos comentarios',
            author=self.user,
            group=self.group,
        ).publish()

        self.thread = ThreadMessage(
            text='Comentario1',
            author=self.user,
            message=self.message,
        ).publish()
        self.liked_thread = ThreadMessage(
            text='Este mensaje sera likeado',
            author=self.user,
            message=self.message,
        ).publish()
        # self.liked_thread.likers.add(self.user)

    def test_create_thread(self):
        view = views.post_comment
        data = {
            'user_id': self.user.id,
            'message_id': self.message.id,
            'text': 'Esto es un comentario woohoo! #primerthread',
        }
        request = self.factory.post('/message/comment/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        expected_response = {
            'author': self.user.id,
            'message': self.message.id,
            'text': 'Esto es un comentario woohoo! #primerthread',
            'likes': 0,
            'dislikes': 0,
            'hashtags': [
                {'id': 1, 'text': 'primerthread'},
            ],
            'mentions': [],
            'likers': [],
            'dislikers': [],
        }
        self.assertEqual(response.status_code, 201)
        created_thread = ThreadMessageSerializer(
            ThreadMessage.objects.get(id=parsed_response['id'])).data
        for key in expected_response:
            self.assertEqual(expected_response[key], parsed_response[key])
            self.assertEqual(expected_response[key], created_thread[key])

    @skipIf(True, "Doesn't exist yet?")
    def test_get_thread(self):
        view = views.get_thread
        data = {'thread_id': self.thread.id}
        request = self.factory.get('/thread/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = {
            'id': self.thread.id,
            'author': self.user.id,
            'group': self.group.id,
            'text': self.thread.text,
            'likes': self.thread.likes,
            'dislikes': self.thread.dislikes,
            'hashtags': [
                {'id': 1, 'text': 'wena!'},
            ],
            'mentions': [
                {'id': self.user.id, 'username': self.user.username},
            ],
            'likers': [],
            'dislikers': [],
            'threads': [],
        }
        self.assertEqual(response.status_code, 200)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

    def test_update_thread(self):
        view = views.post_comment
        data = {
            'thread_id': self.thread.id,
            'text': 'mensaje editado!',
        }
        request = self.factory.patch('/message/comment/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        expected_response = {
            'id': self.thread.id,
            'author': self.user.id,
            'message': self.message.id,
            'text': 'mensaje editado!',
            'likes': self.thread.likes,
            'dislikes': self.thread.dislikes,
            'hashtags': [],
            'mentions': [],
            'likers': [],
            'dislikers': [],
        }
        self.assertEqual(response.status_code, 200)
        updated_thread = ThreadMessageSerializer(
            ThreadMessage.objects.get(id=self.thread.id)).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])
            self.assertEqual(parsed_response[key], updated_thread[key])

    def test_delete_thread(self):
        view = views.post_comment
        data = {'thread_id': self.thread.id}
        request = self.factory.delete('/message/comment/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = STATUS_CODE_200_DELETE

        self.assertEqual(response.status_code, 200)
        self.assertEqual(parsed_response, expected_response)
        with self.assertRaises(ThreadMessage.DoesNotExist):
            deleted_thread = ThreadMessage.objects.get(id=self.thread.id)

    @skipIf(True, "Should Develop GET and Switch POST to other Endpoint")
    def test_thread_not_found(self):
        view = views.post_comment
        data = {'thread_id': 50}

        expected_response = STATUS_CODE_404

        # GET
        request = self.factory.get('/message/comment/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

        # PATCH
        request = self.factory.patch('/message/comment/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

        # DELETE
        request = self.factory.delete('/message/comment/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

    @skipIf(True, "Should Figure Out Once New Endpoint is created")
    def test_post_is_not_allowed(self):
        view = views.post_comment
        data = {
            'user_id': self.user.id,
            'group_id': self.group.id,
            'text': 'Otro comentairio de #ejemplo',
        }
        request = self.factory.post('/thread/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        expected_response = STATUS_CODE_405
        self.assertEqual(response.status_code, 405)
        self.assertEqual(parsed_response, expected_response)

    def test_react_to_thread(self):
        reaction_view = views.thread_reactions

        # Like
        data = {'thread_id': self.thread.id, 'user_id': self.user.id,
                'reaction_type': 1}
        expected_response = {
            'id': self.thread.id,
            'author': self.user.id,
            'message': self.message.id,
            'text': self.thread.text,
            'likes': 1,
            'dislikes': 0,
            'hashtags': [],
            'mentions': [],
            'likers': [
                {'id': self.user.id, 'username': self.user.username},
            ],
            'dislikers': [],
        }
        request = self.factory.post('/messages/comment/reactions/', data, format='json')
        response = reaction_view(request)
        parsed_response = json.loads(response.content)

        # Check response and DB Data
        self.assertEqual(response.status_code, 201)
        db_data = ThreadMessageSerializer(
            ThreadMessage.objects.get(id=self.thread.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])
            self.assertEqual(db_data[key], expected_response[key])
        # Can't Dislike
        data = {'thread_id': self.thread.id, 'user_id': self.user.id}
        request = self.factory.post('/messages/comment/reactions/', data, format='json')
        response = reaction_view(request)
        parsed_response = json.loads(response.content)
        expected_response = STATUS_CODE_403
        self.assertEqual(response.status_code, 403)
        self.assertEqual(parsed_response, expected_response)
        # Unlike
        data = {'thread_id': self.thread.id, 'user_id': self.user.id}
        expected_response = {
            'id': self.thread.id,
            'author': self.user.id,
            'message': self.message.id,
            'text': self.thread.text,
            'likes': 0,
            'dislikes': 0,
            'hashtags': [],
            'mentions': [],
            'likers': [],
            'dislikers': [],
        }
        request = self.factory.post('/messages/comment/reactions/', data, format='json')
        response = reaction_view(request)
        parsed_response = json.loads(response.content)

        # Check response and DB Data
        self.assertEqual(response.status_code, 201)
        db_data = ThreadMessageSerializer(
            ThreadMessage.objects.get(id=self.thread.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])
            self.assertEqual(db_data[key], expected_response[key])
        # Dislike
        data = {'thread_id': self.thread.id, 'user_id': self.user.id,
                'reaction_type': 2}
        expected_response = {
            'id': self.thread.id,
            'author': self.user.id,
            'message': self.message.id,
            'text': self.thread.text,
            'likes': 0,
            'dislikes': 1,
            'hashtags': [],
            'mentions': [],
            'likers': [],
            'dislikers': [
                {'id': self.user.id, 'username': self.user.username},
            ],
        }
        request = self.factory.post('/messages/comment/reactions/', data, format='json')
        response = reaction_view(request)
        parsed_response = json.loads(response.content)

        # Check response and DB Data
        self.assertEqual(response.status_code, 201)
        db_data = ThreadMessageSerializer(
            ThreadMessage.objects.get(id=self.thread.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])
            self.assertEqual(db_data[key], expected_response[key])

    def test_get_thread_reactions(self):
        view = views.thread_reactions
        data = {'thread_id': self.liked_thread.id}
        request = self.factory.get('/message/comment/reactions', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = {
            'id': self.liked_thread.id,
            'likes': 1,
            'dislikes': 0,
            'likers': [
                {'id': self.user.id, 'username': self.user.username},
            ],
            'dislikers': [],
        }

        self.assertEqual(response.status_code, 200)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])


class SearchTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.group = Group.objects.create(
            name='cabros',
            description='Grupo de cabros'
        )
        self.user = User.objects.create(
            username='raiperez',
            first_name='Raimundo',
            last_name='Perez',
            email='mimail2@uc.cl',
            password='password',
        )
        self.non_posting_user = User.objects.create(
            username='noposteo',
            first_name='Yo No',
            last_name='Posteo',
            email='postingisfordummies@uc.cl',
            password='password',
        )
        self.message = Message(
            text='Mensaje woohoo #wena!  @raiperez jeje @hola',
            author=self.user,
            group=self.group,
        ).publish()
        self.message2 = Message(
            text='#wena!  Este es otro mensaje conel mismo hashtag',
            author=self.user,
            group=self.group,
        ).publish()
        self.message3 = Message(
            text='Nunca pueden ser demasiados #wena!',
            author=self.user,
            group=self.group,
        ).publish()

    def test_search_hashtag(self):
        view = views.search_hashtag
        data = {
            'text': 'wena!',
        }
        request = self.factory.get('/search/hashtag/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                'id': self.message.id,
                'author': self.user.id,
                'group': self.group.id,
                'text': self.message.text,
                'likes': self.message.likes,
                'dislikes': self.message.dislikes,
                'hashtags': [
                    {'id': 1, 'text': 'wena!'},
                ],
                'mentions': [
                    {'id': self.user.id, 'username': self.user.username},
                ],
                'likers': [],
                'dislikers': [],
                'threads': [],
            },
            {
                'id': self.message2.id,
                'author': self.user.id,
                'group': self.group.id,
                'text': self.message2.text,
                'likes': self.message2.likes,
                'dislikes': self.message2.dislikes,
                'hashtags': [
                    {'id': 1, 'text': 'wena!'},
                ],
                'mentions': [],
                'likers': [],
                'dislikers': [],
                'threads': [],
            },
            {
                'id': self.message3.id,
                'author': self.user.id,
                'group': self.group.id,
                'text': self.message3.text,
                'likes': self.message3.likes,
                'dislikes': self.message3.dislikes,
                'hashtags': [
                    {'id': 1, 'text': 'wena!'},
                ],
                'mentions': [],
                'likers': [],
                'dislikers': [],
                'threads': [],
            },
        ]

        for expected_message, received_message in zip(expected_response, parsed_response):
            for key in expected_message:
                self.assertEqual(received_message[key], expected_message[key])

    def test_no_matching_hashtags(self):
        view = views.search_hashtag
        data = {
            'text': 'hashtag_inexistente',
        }
        request = self.factory.get('/search/hashtag/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        expected_response = []

        self.assertEqual(expected_response, parsed_response)

    def test_search_username(self):
        view = views.search_username
        data = {
            'username': self.user.username,
        }
        request = self.factory.get('/search/username/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                'id': self.message.id,
                'author': self.user.id,
                'group': self.group.id,
                'text': self.message.text,
                'likes': self.message.likes,
                'dislikes': self.message.dislikes,
                'hashtags': [
                    {'id': 1, 'text': 'wena!'},
                ],
                'mentions': [
                    {'id': self.user.id, 'username': self.user.username},
                ],
                'likers': [],
                'dislikers': [],
                'threads': [],
            },
            {
                'id': self.message2.id,
                'author': self.user.id,
                'group': self.group.id,
                'text': self.message2.text,
                'likes': self.message2.likes,
                'dislikes': self.message2.dislikes,
                'hashtags': [
                    {'id': 1, 'text': 'wena!'},
                ],
                'mentions': [],
                'likers': [],
                'dislikers': [],
                'threads': [],
            },
            {
                'id': self.message3.id,
                'author': self.user.id,
                'group': self.group.id,
                'text': self.message3.text,
                'likes': self.message3.likes,
                'dislikes': self.message3.dislikes,
                'hashtags': [
                    {'id': 1, 'text': 'wena!'},
                ],
                'mentions': [],
                'likers': [],
                'dislikers': [],
                'threads': [],
            },
        ]

        for expected_message, received_message in zip(expected_response, parsed_response):
            for key in expected_message:
                self.assertEqual(received_message[key], expected_message[key])

    def test_no_matching_usernames(self):
        view = views.search_username
        data = {
            'username': self.non_posting_user.username,
        }
        request = self.factory.get('/search/username/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        expected_response = []

        self.assertEqual(expected_response, parsed_response)
