from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="caparanaense")
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                            about="#1 platform",
                                                            website="https://netflix.com")
    
    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 platform",
            "website": "https://netflix.com"
        }
        response = self.client.post(reverse('stream-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('stream-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="caparanaense")
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                        about="#1 platform", website="https://netflix.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="example", storyline="..",
                                                        active=True)
    
    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "Cars 3",
            "storyline": "example",
            "active": True
        }
        response = self.client.post(reverse('movie-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-detail', args=(self.watchlist.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, "example")
        self.assertEqual(models.WatchList.objects.count(), 1)


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="caparanaense")
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                        about="#1 platform", website="https://netflix.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="example", storyline="..",
                                                        active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title="example", storyline="..",
                                                        active=True)
        self.review = models.Review.objects.create(review_user=self.user, rating=5, description="bom",
                                                    watchlist=self.watchlist2, active=True)

    def test_review_create(self):
        data = {
            "user": self.user,
            "rating": 5,
            "description": "Bom",
            "watchlist": self.watchlist,
            "active": True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # segunda requisição
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            "user": self.user,
            "rating": 5,
            "description": "Bom",
            "watchlist": self.watchlist,
            "active": True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "user": self.user,
            "rating": 4,
            "description": "Mais ou menos",
            "watchlist": self.watchlist2,
            "active": True
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
