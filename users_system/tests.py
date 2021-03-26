import json

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.hashers import make_password

from .models import User
from .serializers import UserSerializer


class UserTest(APITestCase):

    def setUp(self):
        admin = User.objects.create(email='admin@gmail.com', password=make_password('admin98'))
        self.client.force_authenticate(user=admin)
        self.mario = User.objects.create(email='magotor1304@gmail.com', password=make_password('pacheco98'))
        self.cesar = User.objects.create(email='cesar98@gmail.com', password=make_password('cesar98'))
        self.rodrigo = User.objects.create(email='rodrigo@gmail.com', password=make_password('rodrigo98'))
        self.valid_user = {
            'email': 'carazas@gmail.com',
            'password': 'carazas98'
        }
        self.invalid_user = {
            'name': 'kurt@gmail.com',
            'password': ''
        }

    def test_get_valid_single_user(self):
        response = self.client.get(reverse('user_detail', kwargs={'user_id': self.mario.id}))
        user = User.objects.get(id=self.mario.id)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_user(self):
        response = self.client.get(reverse('user_detail', kwargs={'user_id': 9}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_user(self):
        response = self.client.post(
            reverse('register'),
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = self.client.post(
            reverse('register'),
            data=json.dumps(self.invalid_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_user(self):
        response = self.client.put(
            reverse('user_detail', kwargs={'user_id': self.mario.id}),
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_user(self):
        response = self.client.put(
            reverse('user_detail', kwargs={'user_id': self.mario.id}),
            data=json.dumps(self.invalid_user),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
