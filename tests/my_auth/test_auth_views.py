from rest_framework import status
from unittest.mock import patch
from django.contrib.auth import SESSION_KEY

from my_auth.models import User
from tests.my_auth.base import BaseUserTest


class TestLoginView(BaseUserTest):

    def custom_authentication(self, username, password):
        data = {
            "username": username,
            "password": password,

        }
        return self.client.post(self.login_url, data)

    def test_login_success(self):
        response = self.custom_authentication(
            username=self.user.username,
            password=self.password
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED,
                         f'Expected 202, received {response.status_code}')
        username_response = response.data['username']
        self.assertEqual(
            username_response,
            User.objects.get(username=username_response).username
        )
        id_response = response.data['id']
        self.assertEqual(
            id_response,
            User.objects.get(id=id_response).id
        )

    def test_login_password_failed(self):
        response = self.custom_authentication(
            username="TestUsername",
            password=self.password
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f'Expected 400, received {response.status_code}')
        self.assertEqual(
            response.json(), {
                'non_field_errors':
                    ['Access denied: wrong username or password.']
                    }
        )

    def test_login_username_failed(self):
        response = self.custom_authentication(
            username="TestUsername",
            password=self.password
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f'Expected 400, received {response.status_code}')
        self.assertEqual(
            response.json(), {
                'non_field_errors':
                    ['Access denied: wrong username or password.']
                    }
        )

    def test_login_two_users_one_by_one(self):
        """
        We attempt to login in 2 users. One by one.
        self.user and self.other_user
        Then check a session status, by compering received ids and user's one.
        """
        response_user_login = self.custom_authentication(
            password=self.password,
            username=self.user.username
        )
        self.assertEqual(
            response_user_login.status_code,
            status.HTTP_202_ACCEPTED
        )
        self.assertEqual(response_user_login.data['id'], self.user.id)
        self.assertEqual(
            response_user_login.data['username'],
            self.user.username
        )
        self.assertEqual(
            int(self.client.session[SESSION_KEY]),
            response_user_login.wsgi_request.user.id
        )

        response_other_user_login = self.custom_authentication(
            password=self.password,
            username=self.other_user.username
        )
        self.assertEqual(
            response_other_user_login.status_code,
            status.HTTP_202_ACCEPTED
        )
        self.assertEqual(
            response_other_user_login.data['username'],
            self.other_user.username
        )
        self.assertEqual(
            response_other_user_login.data['username'],
            self.other_user.username
        )

        self.assertNotEqual(
            int(self.client.session[SESSION_KEY]),
            response_user_login.wsgi_request.user.id
        )
        self.assertEqual(
            int(self.client.session[SESSION_KEY]),
            response_other_user_login.wsgi_request.user.id
        )

    def test_login_empty_data_provided(self):
        response = self.custom_authentication(password="", username="")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f'Expected 400, received {response.status_code}')
        self.assertEqual(str(response.data['username'][0]),
                         'This field may not be blank.')
        self.assertEqual(str(response.data['password'][0]),
                         'This field may not be blank.')


class TestLogoutView(BaseUserTest):

    def test_logout_user_success(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, None)


class TestRegisterView(BaseUserTest):

    def custom_sign_up(self, username, password, email):
        data = {
            "username": username,
            "password": password,
            "email": email
        }
        return self.client.post(self.register_url, data)

    def test_register_success(self):
        response = self.custom_sign_up("Test", "TestPass123", "12@icloud.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f'Expected 201, received {response.status_code}')
        self.assertEqual(response.data['username'], "Test")

    def test_with_wrong_password_lenght_register_failed(self):
        response = self.custom_sign_up("Test", "1234", "12@icloud.com")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f'Expected 400, received {response.status_code}')
        self.assertEqual(
            response.data['password'][0],
            'This password is too short. It must contain at least 8 characters.'
        )

    def test_sign_up_and_user_is_still_login(self):
        sign_up_response = self.custom_sign_up(
            username="Test",
            password=self.password,
            email="12@icloud.com"
        )
        self.assertEqual(
            sign_up_response.status_code, status.HTTP_201_CREATED,
            f'''Expected 201, received
            {sign_up_response.status_code}
            '''
        )
        session_user_id = int(self.client.session[SESSION_KEY])
        self.assertEqual(
            sign_up_response.wsgi_request.user.id,
            session_user_id
        )
        self.assertTrue(sign_up_response.wsgi_request.user.is_authenticated)

    def test_same_username_register(self):
        sign_up_user = self.custom_sign_up(
            username="Test",
            password=self.password,
            email="12@icloud.com"
        )
        self.assertEqual(sign_up_user.status_code, status.HTTP_201_CREATED,
                         f'Expected 201, received {sign_up_user.status_code}')
        sign_up_other_user = self.custom_sign_up(
            username="Test",
            password=self.password,
            email="10@icloud.com"
        )

        self.assertEqual(
            sign_up_other_user.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected 400, received {sign_up_other_user.status_code}'
        )
        self.assertEqual(
            ''.join(sign_up_other_user.data['username']),
            'A user with that username already exists.'
        )

    def test_wrong_email_format(self):
        sign_up_other_user = self.custom_sign_up(
            username="Test1",
            password=self.password,
            email="11@icloudcom"
        )
        self.assertEqual(
            sign_up_other_user.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected 400, received {sign_up_other_user.status_code}'
        )

        self.assertEqual(
            ''.join(sign_up_other_user.data['email']),
            'Enter a valid email address.'
        )

    def test_not_ununique_email(self):
        sign_up_user = self.custom_sign_up(
            username="Test",
            password=self.password,
            email="11@icloud.com"
        )
        self.assertEqual(sign_up_user.status_code, status.HTTP_201_CREATED,
                         f'Expected 201, received {sign_up_user.status_code}')
        sign_up_other_user = self.custom_sign_up(
            username="Test1",
            password=self.password,
            email="11@icloud.com"
        )

        self.assertEqual(
            sign_up_other_user.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected 400, received {sign_up_other_user.status_code}'
        )
        self.assertEqual(
            ''.join(sign_up_other_user.data['email']),
            'User with this email address already exists.'
        )
