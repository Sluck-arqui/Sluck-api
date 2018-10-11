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
            User.objects.get(username="nachocontreras")).data
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

        expected_response = {'status_text': 'Unauthorized'}
        self.assertEqual(response.status_code, 401)

    def test_get_is_unauthorized(self):
        view = views.register
        request = self.factory.get('/register/')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = {'status_text': 'Unauthorized'}
        self.assertEqual(response.status_code, 401)
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
            'email': 'mail@mail.com',
            'password': 'contraseña',
        }
        request = self.factory.patch('/user/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = {
            'id': self.user.id,
            'username': 'raiperez',
            'first_name': 'raimundo',
            'last_name': 'perez',
            'email': 'mail@mail.com',
            'password': 'contraseña',
        }

        self.assertEqual(response.status_code, 200)
        for key in expected_response:
            self.assertEqual(parsed_response[key], expected_response[key])

    def test_delete_user(self):
        view = views.get_user
        data = {'user_id': self.user.id}
        request = self.factory.delete('/user/', data, format='json')
        response = view(request)
        parsed_response = json.loads(response.content)

        expected_response = {'status_text': 'Deleted successfully'}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(parsed_response, expected_response)

    def test_user_not_found(self):
        view = views.get_user
        data = {'user_id': 50}

        expected_response = {'status_text': 'Object user not found'}

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

    def test_post_is_unauthorized(self):
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
        expected_response = {'status_text': 'Unauthorized'}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(parsed_response, expected_response)
