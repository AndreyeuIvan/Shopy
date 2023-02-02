from rest_framework import status
from django.urls import reverse

from my_auth.models import User
from tests.my_auth.base import BaseUserTest


class TestUserView(BaseUserTest):
    def test_list_api_get_success(self):
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.all().count())
        user_id = self.user.id
        list_users = response.data
        self.assertTrue(any(user_id == dict_["id"] for dict_ in list_users))

    def test_detail_api_get_success(self):
        response = self.client.get(reverse("user", args=(self.user.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        username_response = response.data["username"]
        self.assertEqual(
            username_response, User.objects.get(username=username_response).username
        )
        id_response = response.data["id"]
        self.assertEqual(id_response, User.objects.get(id=id_response).id)

    def test_get_request_for_auth_user(self):
        response = self.client.get(reverse("users"))
        self.client.force_login(self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = self.user.id
        list_users = response.data
        self.assertTrue(any(user_id == dict_["id"] for dict_ in list_users))

    def test_get_request_for_unauth_user(self):
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = self.user.id
        list_users = response.data
        self.assertFalse(any(user_id in dict_ for dict_ in list_users))
