import json
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from locations.models import Region, Province, District
from accounts.models import User, Profile, Musician
from .models import Publication, Comment, Notification, Following, Genre, Instrument
from .serializers import PublicationSerializer, CommentSerializer, NotificationSerializer, \
    GenreSerializer, InstrumentSerializer, FollowedSerializer, FollowerSerializer


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
        self.noli_musician = Musician.objects.create(first_name='sebastian', last_name='noli', birth_date='01/10/2001',
                                                     phone='988380177', type='Musician', user=self.noli,
                                                     district=self.los_olivos)
        self.rock = Genre.objects.create(name='rock')
        self.pop = Genre.objects.create(name='pop')
        self.electro = Genre.objects.create(name='electro')
        self.metal = Genre.objects.create(name='metal')
        self.mario_musician.genres.add(self.rock)
        self.mario_musician.genres.add(self.pop)
        self.noli_musician.genres.add(self.rock)

    def test_get_all_genres(self):
        response = self.client.get(reverse('genres_list'))
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_genres_by_musician(self):
        response = self.client.get(reverse('list_genres_by_musician',
                                           kwargs={'musician_id': self.mario_musician.user.id}))
        musician_genres = Genre.objects.filter(musicians__user=self.mario_musician.user.id)
        serializer = GenreSerializer(musician_genres, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_musicians_genres(self):
        response = self.client.post(
            reverse('musicians_genres', kwargs={'musician_id': self.noli_musician.user.id,
                                                'genre_id': self.pop.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_musicians_genres(self):
        response = self.client.post(
            reverse('musicians_genres', kwargs={'musician_id': self.noli_musician.user.id,
                                                'genre_id': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_valid_musicians_genres(self):
        response = self.client.delete(
            reverse('musicians_genres', kwargs={'musician_id': self.mario_musician.user.id,
                                                'genre_id': self.pop.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_musicians_genres(self):
        response = self.client.delete(
            reverse('musicians_genres', kwargs={'musician_id': self.mario_musician.user.id,
                                                'genre_id': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
                                           kwargs={'musician_id': self.mario_musician.user.id}))
        musician_instruments = Instrument.objects.filter(musicians__user=self.mario_musician.user.id)
        serializer = InstrumentSerializer(musician_instruments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_musicians_instruments(self):
        response = self.client.post(
            reverse('musicians_instruments', kwargs={'musician_id': self.noli_musician.user.id,
                                                     'instrument_id': self.ukulele.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_musicians_instruments(self):
        response = self.client.post(
            reverse('musicians_instruments', kwargs={'musician_id': self.noli_musician.user.id,
                                                     'instrument_id': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_valid_musicians_instruments(self):
        response = self.client.delete(
            reverse('musicians_instruments', kwargs={'musician_id': self.mario_musician.user.id,
                                                     'instrument_id': self.ukulele.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_musicians_instruments(self):
        response = self.client.delete(
            reverse('musicians_instruments', kwargs={'musician_id': self.mario_musician.user.id,
                                                     'instrument_id': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
                                           kwargs={'musician_id': self.mario_musician.user.id}))
        publications = Publication.objects.filter(musician__user=self.mario_musician.user.id)
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
            reverse('musician_publications', kwargs={'musician_id': self.mario_musician.user.id}),
            data=json.dumps(self.valid_publication),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_publication(self):
        response = self.client.post(
            reverse('musician_publications', kwargs={'musician_id': self.mario_musician.user.id}),
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
                                               'commenter_id': self.noli_profile.user.id}),
            data=json.dumps(self.valid_comment),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_comment(self):
        response = self.client.post(
            reverse('create_comments', kwargs={'publication_id': self.publication_one.id,
                                               'commenter_id': self.noli_profile.user.id}),
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


class FollowingTest(APITestCase):
    def setUp(self):
        admin = User.objects.create(email='admin@gmail.com', password=make_password('admin98'))
        self.client.force_authenticate(user=admin)
        self.region_lima = Region.objects.create(name='Lima')
        self.province_lima = Province.objects.create(name='Lima', region=self.region_lima)
        self.los_olivos = District.objects.create(name='Los olivos', province=self.province_lima)
        self.mario = User.objects.create(email='magotor1304@gmail.com', password=make_password('pacheco98'))
        self.cesar = User.objects.create(email='cesar98@gmail.com', password=make_password('cesar98'))
        self.rodrigo = User.objects.create(email='rodrigo@gmail.com', password=make_password('rodrigo98'))
        self.mario_musician = Musician.objects.create(first_name='mario', last_name='tataje', birth_date='13/04/2000',
                                                      phone='995995408', type='Musician', user=self.mario,
                                                      district=self.los_olivos)
        self.cesar_musician = Musician.objects.create(first_name='cesar', last_name='ramirez', birth_date='21/03/1996',
                                                      phone='927528321', type='Musician', user=self.cesar,
                                                      district=self.los_olivos)
        self.rodrigo_musician = Musician.objects.create(first_name='rodrigo', last_name='silva',
                                                        birth_date='04/07/2001',
                                                        phone='940199246', type='Musician', user=self.rodrigo,
                                                        district=self.los_olivos)
        self.following_one = Following.objects.create(follower=self.mario_musician, followed=self.cesar_musician)
        self.following_two = Following.objects.create(follower=self.mario_musician, followed=self.rodrigo_musician)
        self.following_three = Following.objects.create(follower=self.cesar_musician, followed=self.mario_musician)
        self.following_four = Following.objects.create(follower=self.rodrigo_musician, followed=self.mario_musician)

    def test_get_all_followed_by_follower(self):
        response = self.client.get(reverse('list_followed_by_musician',
                                           kwargs={'musician_id': self.mario_musician.user.id}))
        followed = Following.objects.filter(follower_id=self.mario_musician.user.id)
        serializer = FollowedSerializer(followed, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_follower_by_followed(self):
        response = self.client.get(reverse('list_follower_by_musician',
                                           kwargs={'musician_id': self.mario_musician.user.id}))
        followers = Following.objects.filter(followed_id=self.mario_musician.user.id)
        serializer = FollowerSerializer(followers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_following(self):
        response = self.client.post(
            reverse('create_delete_following', kwargs={'follower_id': self.cesar_musician.user.id,
                                                       'followed_id': self.rodrigo_musician.user.id}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_following(self):
        response = self.client.post(
            reverse('create_delete_following', kwargs={'follower_id': self.mario_musician.user.id,
                                                       'followed_id': 80}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_valid_following(self):
        response = self.client.delete(
            reverse('create_delete_following', kwargs={'follower_id': self.mario_musician.user.id,
                                                       'followed_id': self.cesar_musician.user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_following(self):
        response = self.client.delete(
            reverse('create_delete_following', kwargs={'follower_id': self.mario_musician.user.id,
                                                       'followed_id': 200}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NotificationTest(APITestCase):
    def setUp(self):
        admin = User.objects.create(email='admin@gmail.com', password=make_password('admin98'))
        self.client.force_authenticate(user=admin)
        self.region_lima = Region.objects.create(name='Lima')
        self.province_lima = Province.objects.create(name='Lima', region=self.region_lima)
        self.los_olivos = District.objects.create(name='Los olivos', province=self.province_lima)
        self.mario = User.objects.create(email='magotor1304@gmail.com', password=make_password('pacheco98'))
        self.cesar = User.objects.create(email='cesar98@gmail.com', password=make_password('cesar98'))
        self.mario_profile = Profile.objects.create(first_name='mario', last_name='tataje', birth_date='13/04/2000',
                                                    phone='995995408', type='Musician', user=self.mario,
                                                    district=self.los_olivos)
        self.cesar_profile = Profile.objects.create(first_name='cesar', last_name='ramirez', birth_date='21/03/1996',
                                                    phone='927528321', type='Organizer', user=self.cesar,
                                                    district=self.los_olivos)

    def test_get_all_notifications_by_profile(self):
        response = self.client.get(reverse('list_notification_by_profile',
                                           kwargs={'profile_id': self.mario_profile.user.id}))
        notifications = Notification.objects.filter(profile__user=self.mario_profile.user.id)
        serializer = NotificationSerializer(notifications, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
