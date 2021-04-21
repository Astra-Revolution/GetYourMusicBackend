import json

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.hashers import make_password

from .models import User, Profile, Musician, Organizer
from locations.models import Region, Province, District
from .serializers import UserSerializer, ProfileSerializer, MusicianSerializer, OrganizerSerializer


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


class ProfileTest(APITestCase):

    def setUp(self):
        admin = User.objects.create(email='admin@gmail.com', password=make_password('admin98'))
        self.client.force_authenticate(user=admin)
        self.region_lima = Region.objects.create(name='Lima')
        self.province_lima = Province.objects.create(name='Lima', region=self.region_lima)
        self.los_olivos = District.objects.create(name='Los olivos', province=self.province_lima)
        self.mario = User.objects.create(email='magotor1304@gmail.com', password=make_password('pacheco98'))
        self.cesar = User.objects.create(email='cesar98@gmail.com', password=make_password('cesar98'))
        self.rodrigo = User.objects.create(email='rodrigo@gmail.com', password=make_password('rodrigo98'))
        self.noli = User.objects.create(email='noli@gmail.com', password=make_password('noli98'))
        self.dalembert = User.objects.create(email='dalembert@gmail.com', password=make_password('dalembert98'))
        self.mario_profile = Profile.objects.create(first_name='mario', last_name='tataje', birth_date='13/04/2000',
                                                    phone='995995408', type='Musician', user=self.mario,
                                                    district=self.los_olivos)
        self.cesar_profile = Profile.objects.create(first_name='cesar', last_name='ramirez', birth_date='21/03/1996',
                                                    phone='927528321', type='Organizer', user=self.cesar,
                                                    district=self.los_olivos)
        self.rodrigo_profile = Profile.objects.create(first_name='rodrigo', last_name='silva', birth_date='04/07/2001',
                                                      phone='940199246', type='Organizer', user=self.rodrigo,
                                                      district=self.los_olivos)
        self.noli_profile = Profile.objects.create(first_name='sebastian', last_name='noli', birth_date='01/10/2001',
                                                   phone='988380177', type='Musician', user=self.noli,
                                                   district=self.los_olivos)
        self.valid_profile = {
            'first_name': 'dalembert',
            'last_name': 'monzon',
            'birth_date': '24/09/2020',
            'phone': '998869900',
            'type': 'Musician',
            'district_id': self.los_olivos.id
        }
        self.invalid_profile = {
            'first_name': 'dalembert',
            'last_name': '',
            'birth_date': '24/09/2020',
            'phone': '998869900',
            'type': 'Musician',
            'district_id': 1
        }

    def test_get_all_profiles(self):
        response = self.client.get(reverse('profiles_list'))
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_profile(self):
        response = self.client.get(reverse('profile_detail', kwargs={'profile_id': self.mario_profile.user.id}))
        profile = Profile.objects.get(user=self.mario_profile.user.id)
        serializer = ProfileSerializer(profile)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_profile(self):
        response = self.client.get(reverse('profile_detail', kwargs={'profile_id': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_profile(self):
        response = self.client.post(
            reverse('create_profiles', kwargs={'user_id': self.dalembert.id}),
            data=json.dumps(self.valid_profile),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_profile(self):
        response = self.client.post(
            reverse('create_profiles', kwargs={'user_id': self.dalembert.id}),
            data=json.dumps(self.invalid_profile),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_profile(self):
        response = self.client.put(
            reverse('profile_detail', kwargs={'profile_id': self.mario_profile.user.id}),
            data=json.dumps(self.valid_profile),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_profile(self):
        response = self.client.put(
            reverse('profile_detail', kwargs={'profile_id': self.mario_profile.user.id}),
            data=json.dumps(self.invalid_profile),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MusicianTest(APITestCase):
    def setUp(self):
        admin = User.objects.create(email='admin@gmail.com', password=make_password('admin98'))
        self.client.force_authenticate(user=admin)
        self.region_lima = Region.objects.create(name='Lima')
        self.province_lima = Province.objects.create(name='Lima', region=self.region_lima)
        self.los_olivos = District.objects.create(name='Los olivos', province=self.province_lima)
        self.mario = User.objects.create(email='magotor1304@gmail.com', password=make_password('pacheco98'))
        self.noli = User.objects.create(email='noli@gmail.com', password=make_password('noli98'))
        self.mario_musician = Musician.objects.create(first_name='mario', last_name='tataje', birth_date='13/04/2000',
                                                      phone='995995408', type='Musician', user=self.mario,
                                                      district=self.los_olivos)
        self.noli_musician = Musician.objects.create(first_name='sebastian', last_name='noli', birth_date='01/10/2001',
                                                     phone='988380177', type='Musician', user=self.noli,
                                                     district=self.los_olivos)

    def test_get_all_musicians(self):
        response = self.client.get(reverse('musicians_list'))
        musicians = Musician.objects.all()
        serializer = MusicianSerializer(musicians, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_musicians(self):
        response = self.client.post(reverse('musician_filter'),
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrganizerTest(APITestCase):
    def setUp(self):
        admin = User.objects.create(email='admin@gmail.com', password=make_password('admin98'))
        self.client.force_authenticate(user=admin)
        self.region_lima = Region.objects.create(name='Lima')
        self.province_lima = Province.objects.create(name='Lima', region=self.region_lima)
        self.los_olivos = District.objects.create(name='Los olivos', province=self.province_lima)
        self.cesar = User.objects.create(email='cesar98@gmail.com', password=make_password('cesar98'))
        self.rodrigo = User.objects.create(email='rodrigo@gmail.com', password=make_password('rodrigo98'))
        self.cesar_profile = Profile.objects.create(first_name='cesar', last_name='ramirez', birth_date='21/03/1996',
                                                    phone='927528321', type='Organizer', user=self.cesar,
                                                    district=self.los_olivos)
        self.rodrigo_profile = Profile.objects.create(first_name='rodrigo', last_name='silva', birth_date='04/07/2001',
                                                      phone='940199246', type='Organizer', user=self.rodrigo,
                                                      district=self.los_olivos)

    def test_get_all_organizers(self):
        response = self.client.get(reverse('organizers_list'))
        organizers = Organizer.objects.all()
        serializer = OrganizerSerializer(organizers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
