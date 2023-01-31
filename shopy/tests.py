from rest_framework.test import APITestCase

from django.urls import reverse
from django.contrib.auth.models import User


class PurchaseListAPIViewTestCase(APITestCase):
    url = reverse()
    def setUp(self):
        self.name = "Potato"
        self.shop_name = "I_LOVE_YOU"
