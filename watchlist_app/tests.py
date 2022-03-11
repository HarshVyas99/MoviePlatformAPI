from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

from rest_framework import status
from rest_framework.test import APITestCase

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username="example",password="NewPassword@123")
        self.token=Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream=models.StreamPlatform.objects.create(name="Netflix",
            about="#1 Streaming Platform",
            website="https://www.netflix.com")

        
    def test_stream_platform_create(self):
        data={
            "name":"Netflix",
            "about":"#1 Streaming Platform",
            "website":"https://www.netflix.com"
        }
        
        response=self.client.post(reverse('streamplatform-list'),data)
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_stream_platform_list(self):
        
        response=self.client.get(reverse('streamplatform-list'))
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        
    def test_stream_platform_detail_ind(self):
        response=self.client.get(reverse('streamplatform-detail',args=(self.stream.id,)))
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        

class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username="example",password="NewPassword@123")
        self.token=Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream=models.StreamPlatform.objects.create(name="Netflix",
            about="#1 Streaming Platform",
            website="https://www.netflix.com")
        self.watch=models.WatchList.objects.create(platform=self.stream,
            title="Example Movie",
            storyline="Example Storyline",
            active=True)    
        
    def test_watchlist_create(self):
        data={
            "platform":self.stream,
            "title":"Example Movie",
            "storyline":"Example Storyline",
            "active":True
        }
        response=self.client.post(reverse('watchlist-list'),data)
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
        
    
    def test_watchlist_list(self):
        
        response=self.client.get(reverse('watchlist-list'))
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        
    def test_watchlist_ind(self):
        
        response=self.client.get(reverse('watchlist-details',args=(self.watch.id,)))
        self.assertEquals(response.status_code,status.HTTP_200_OK)

class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username="example",password="NewPassword@123")
        self.token=Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream=models.StreamPlatform.objects.create(name="Netflix",
            about="#1 Streaming Platform",
            website="https://www.netflix.com")
        self.watch2=models.WatchList.objects.create(platform=self.stream,
            title="Example Movie",
            storyline="Example Storyline",
            active=True)
        self.watch=models.WatchList.objects.create(platform=self.stream,
            title="Example Movie",
            storyline="Example Storyline",
            active=True)
        self.review=models.Review.objects.create(review_user=self.user,
            rating=5,
            description="Great Movie",
            watchlist=self.watch2,
            active=True)   
        
    def test_review_create(self):
        data={
            "review_user":self.user,
            "rating":5,
            "description":"Great Movie",
            "watchlist":self.watch,
            "active":True
        }
        response=self.client.post(reverse('review-create',args=(self.watch.id,)),data)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        
        response=self.client.post(reverse('review-create',args=(self.watch.id,)),data)
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_unauth(self):
        data={
            "review_user":self.user,
            "rating":5,
            "description":"Great Movie",
            "watchlist":self.watch,
            "active":True
        }
        
        self.client.force_authenticate(user=None)
        response=self.client.post(reverse('review-create',args=(self.watch.id,)),data)
        self.assertEquals(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
        
    def test_review_update(self):
        data={
            "review_user":self.user,
            "rating":4,
            "description":"Great Movie - Updated!",
            "watchlist":self.watch2,
            "active":False
        }
        response=self.client.put(reverse('review-detail',args=(self.watch2.id,)),data)
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        
    def test_review_list(self):
        response=self.client.get(reverse('review-list',args=(self.review.id,)))
        self.assertEquals(response.status_code,status.HTTP_200_OK)        

    def test_review_user(self):
        response=self.client.get('/watch/'+str(self.watch.id)+'/reviews-list/?review_user__username',args=(self.user.username))
        
        self.assertEquals(response.status_code,status.HTTP_200_OK)