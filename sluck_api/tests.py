from django.test import TestCase
from rest_framework.test import APIRequestFactory
import sluck_api.views as views
from unittest import skip
import json
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
    ThreadMessageSerializer,
)
from .utils import (
    STATUS_CODE_200_DELETE,
    STATUS_CODE_400,
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
            User.objects.get(id=parsed_response['id'])).data
        for key in data:
            self.assertEqual(data[key], parsed_response[key])
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

    def test_get_user(self):
        view = views.get_user
        data = {'user_id': self.user.id}
        request = self.factory.get('/user/', data, format='json')
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
        request = self.factory.patch('/user/', data, format='json')
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
        request = self.factory.delete('/user/', data, format='json')
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
        request = self.factory.get('/user/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

        # PATCH
        request = self.factory.patch('/user/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(parsed_response, expected_response)

        # DELETE
        request = self.factory.delete('/user/', data, format='json')
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
        request = self.factory.post('/user/', data, format='json')
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
        view_get_group = views.get_group

        # Add first member
        data = {'group_id': self.group.id, 'user_id': self.user1.id}
        expected_response = {
            'id': self.group.id,
            'members': [self.user1.id],
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
            'members': [self.user1.id, self.user2.id],
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
            'members': [self.user2.id],
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

    @skip
    def test_message_member(self):
        view = views.message_member
        view_get_message = views.get_message

        # Add first member
        data = {'message_id': self.message.id, 'user_id': self.user1.id}
        expected_response = {
            'id': self.message.id,
            'members': [self.user1.id],
            'description': self.message.description,
            'name': self.message.name,
        }
        request = self.factory.post('/message/member/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        # Check response
        self.assertEqual(response.status_code, 201)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

        # Check DB
        parsed_response = MessageSerializer(
            Message.objects.get(id=self.message.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

        # Add second member
        data = {'message_id': self.message.id, 'user_id': self.user2.id}
        expected_response = {
            'id': self.message.id,
            'members': [self.user1.id, self.user2.id],
            'description': self.message.description,
            'name': self.message.name,
        }
        request = self.factory.post('/message/member/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        # Check response
        self.assertEqual(response.status_code, 201)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

        # Check DB
        parsed_response = MessageSerializer(
            Message.objects.get(id=self.message.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

        # Delete first user
        data = {'message_id': self.message.id, 'user_id': self.user1.id}
        expected_response = {
            'id': self.message.id,
            'members': [self.user2.id],
            'description': self.message.description,
            'name': self.message.name,
        }
        request = self.factory.delete('/message/member/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        # Check response
        self.assertEqual(response.status_code, 200)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

        # Check DB
        parsed_response = MessageSerializer(
            Message.objects.get(id=self.message.id)
        ).data
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])
