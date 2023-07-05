from django.test import TestCase
from django.test.client import Client
from .models import *


class CreateUserTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        City.objects.create(name="Poznan")

    def test_create_user(self):
        response = self.client.post("/register/", {
            "username": "test_user_01",
            "password1": "testpass01",
            "password2": "testpass01",
            "name": "tname01",
            "surname": "tsurname01",
            "email": "test01@mail.com",
            "city": "Poznan"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(user__username="test_user_01").exists())
