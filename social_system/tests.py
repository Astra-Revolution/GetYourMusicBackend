import json
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from locations.models import Region, Province, District
from users_system.models import User, Profile, Musician
from .models import Publication, Comment
from .serializers import PublicationSerializer, CommentSerializer


class PublicationTest(APITestCase):
    def setUp(self):
        admin = User.objects.create(email='admin@gmail.com', password=make_password('admin98'))
        self.client.force_authenticate(user=admin)
        self.region_lima = Region.objects.create(name='Lima')
        self.province_lima = Province.objects.create(name='Lima', region=self.region_lima)
        self.los_olivos = District.objects.create(name='Los olivos', province=self.province_lima)
        self.mario = User.objects.create(email='magotor1304@gmail.com', password=make_password('pacheco98'))
        self.mario_musician = Musician.objects.create(first_name='mario', last_name='tataje', birth_date='13/04/2000',
                                                      phone='995995408', type='Musician', user=self.mario,
                                                      district=self.los_olivos)
        self.publication_one = Publication.objects.create(video_url='this is the url', content='the content',
                                                          musician=self.mario_musician)
        self.publication_two = Publication.objects.create(video_url='this is the url two', content='the content two',
                                                          musician=self.mario_musician)
        self.valid_publication = {
            'video_url': 'this is the valid url',
            'content': 'this is the valid content'
        }
        self.invalid_publication = {
            'video_url': '',
            'content': 'this is the invalid content'
        }

    def test_get_all_publications(self):
        response = self.client.get(reverse('publication_list'))
        publications = Publication.objects.all()
        serializer = PublicationSerializer(publications, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_publications_by_musicians(self):
        response = self.client.get(reverse('musician_publications',
                                           kwargs={'musician_id': self.mario_musician.id}))
        publications = Publication.objects.filter(musician__id=self.mario_musician.id)
        serializer = PublicationSerializer(publications, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_publication(self):
        response = self.client.get(reverse('publication_detail',
                                           kwargs={'publication_id': self.publication_one.id}))
        publication = Publication.objects.get(id=self.publication_one.id)
        serializer = PublicationSerializer(publication)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_publication(self):
        response = self.client.get(reverse('publication_detail',
                                           kwargs={'publication_id': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_publication(self):
        response = self.client.post(
            reverse('musician_publications', kwargs={'musician_id': self.mario_musician.id}),
            data=json.dumps(self.valid_publication),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_publication(self):
        response = self.client.post(
            reverse('musician_publications', kwargs={'musician_id': self.mario_musician.id}),
            data=json.dumps(self.invalid_publication),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_publication(self):
        response = self.client.put(
            reverse('publication_detail', kwargs={'publication_id': self.publication_one.id}),
            data=json.dumps(self.valid_publication),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_publication(self):
        response = self.client.put(
            reverse('publication_detail', kwargs={'publication_id': self.publication_one.id}),
            data=json.dumps(self.invalid_publication),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_publication(self):
        response = self.client.delete(
            reverse('publication_detail', kwargs={'publication_id': self.publication_one.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_publication(self):
        response = self.client.delete(
            reverse('publication_detail', kwargs={'publication_id': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentTest(APITestCase):
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
        self.noli_profile = Profile.objects.create(first_name='sebastian', last_name='noli', birth_date='01/10/2001',
                                                   phone='988380177', type='Musician', user=self.noli,
                                                   district=self.los_olivos)
        self.publication_one = Publication.objects.create(video_url='this is the url', content='the content',
                                                          musician=self.mario_musician)
        self.comment_one = Comment.objects.create(text='this is the comment', publication=self.publication_one,
                                                  commenter=self.noli_profile)
        self.comment_two = Comment.objects.create(text='this is the comment two', publication=self.publication_one,
                                                  commenter=self.noli_profile)
        self.valid_comment = {
            'text': 'this is the valid comment'
        }
        self.invalid_comment = {
            'text': ''
        }

    def test_get_all_comments_by_publication(self):
        response = self.client.get(reverse('list_comments_by_publication',
                                           kwargs={'publication_id': self.publication_one.id}))
        comments = Comment.objects.filter(publication__id=self.publication_one.id)
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_comment(self):
        response = self.client.get(reverse('comment_detail',
                                           kwargs={'comment_id': self.comment_one.id}))
        comment = Comment.objects.get(id=self.comment_one.id)
        serializer = CommentSerializer(comment)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_comment(self):
        response = self.client.get(reverse('comment_detail',
                                           kwargs={'comment_id': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_comment(self):
        response = self.client.post(
            reverse('create_comments', kwargs={'publication_id': self.publication_one.id,
                                               'commenter_id': self.noli_profile.id}),
            data=json.dumps(self.valid_comment),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_comment(self):
        response = self.client.post(
            reverse('create_comments', kwargs={'publication_id': self.publication_one.id,
                                               'commenter_id': self.noli_profile.id}),
            data=json.dumps(self.invalid_comment),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_comment(self):
        response = self.client.put(
            reverse('comment_detail', kwargs={'comment_id': self.comment_one.id}),
            data=json.dumps(self.valid_comment),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_comment(self):
        response = self.client.put(
            reverse('comment_detail', kwargs={'comment_id': self.comment_one.id}),
            data=json.dumps(self.invalid_comment),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_comment(self):
        response = self.client.delete(reverse('comment_detail',
                                              kwargs={'comment_id': self.comment_one.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_comment(self):
        response = self.client.delete(reverse('comment_detail',
                                              kwargs={'comment_id': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
