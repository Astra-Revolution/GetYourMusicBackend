from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from locations.models import Region, Province, District
from .models import Genre, Instrument
from .serializers import GenreSerializer, InstrumentSerializer
from users_system.models import User, Musician


class GenreTest(APITestCase):

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
        self.rock = Genre.objects.create(name='rock')
        self.pop = Genre.objects.create(name='pop')
        self.electro = Genre.objects.create(name='electro')
        self.metal = Genre.objects.create(name='metal')
        self.mario_musician.genres.add(self.rock)
        self.mario_musician.genres.add(self.pop)

    def test_get_all_genres(self):
        response = self.client.get(reverse('genres_list'))
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_genres_by_musician(self):
        response = self.client.get(reverse('list_genres_by_musician',
                                           kwargs={'musician_id': self.mario_musician.id}))
        musician_genres = Genre.objects.filter(musicians__id=self.mario_musician.id)
        serializer = GenreSerializer(musician_genres, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InstrumentTest(APITestCase):

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
        self.guitar = Instrument.objects.create(name='guitar')
        self.ukulele = Instrument.objects.create(name='ukulele')
        self.drums = Instrument.objects.create(name='drums')
        self.piano = Instrument.objects.create(name='piano')
        self.mario_musician.instruments.add(self.guitar)
        self.mario_musician.instruments.add(self.ukulele)
        self.noli_musician.instruments.add(self.guitar)

    def test_get_all_instruments(self):
        response = self.client.get(reverse('instruments_list'))
        instruments = Instrument.objects.all()
        serializer = InstrumentSerializer(instruments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_instruments_by_musician(self):
        response = self.client.get(reverse('list_instruments_by_musician',
                                           kwargs={'musician_id': self.mario_musician.id}))
        musician_instruments = Instrument.objects.filter(musicians__id=self.mario_musician.id)
        serializer = InstrumentSerializer(musician_instruments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
