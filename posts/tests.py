from django.contrib.auth.hashers import make_password
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from posts.models import Post, Like

TEST_EMAIL = 'test@test.test'
TEST_PASS = 'pa55word'

TEST_TITLE = 'Test Title'
TEST_TEXT = 'Test Text. No Lorem ipsum allowed.'


class PostsTests(APITestCase):

    def test_posts_create_post(self):
        user = User.objects.create(email=TEST_EMAIL,
                                   password=make_password(TEST_PASS))

        url = reverse('posts-list')
        data = {
            'title': TEST_TITLE,
            'text': TEST_TEXT
        }

        self.client.force_authenticate(user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        author_id = response.data['author']
        self.assertEqual(author_id, user.id)

    def test_posts_delete_post(self):
        user = User.objects.create(email=TEST_EMAIL,
                                   password=make_password(TEST_PASS))
        post = Post.objects.create(author=user,
                                   title=TEST_TITLE,
                                   text=TEST_TEXT)
        url = reverse('posts-detail', args=[post.id])

        self.client.force_authenticate(user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.all().count(), 0)

    def test_posts_list_posts(self):
        user = User.objects.create(email=TEST_EMAIL,
                                   password=make_password(TEST_PASS))
        Post.objects.create(author=user,
                            title=TEST_TITLE,
                            text=TEST_TEXT)
        url = reverse('posts-list')

        self.client.force_authenticate(user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], TEST_TITLE)
        self.assertEqual(response.data[0]['text'], TEST_TEXT)
        self.assertEqual(response.data[0]['author'], user.id)

    def test_posts_like(self):
        user = User.objects.create(email=TEST_EMAIL,
                                   password=make_password(TEST_PASS))
        post = Post.objects.create(author=user,
                                   title=TEST_TITLE,
                                   text=TEST_TEXT)
        url = reverse('posts-like', args=[post.id])
        data = {
            'post': post.id
        }

        self.client.force_authenticate(user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Post.objects.filter(id=post.id).first().likes.count(), 1)

    def test_posts_dislike(self):
        user = User.objects.create(email=TEST_EMAIL,
                                   password=make_password(TEST_PASS))
        post = Post.objects.create(author=user,
                                   title=TEST_TITLE,
                                   text=TEST_TEXT)
        Like.objects.create(user=user, post=post)
        url = reverse('posts-like', args=[post.id])

        self.client.force_authenticate(user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Post.objects.filter(id=post.id).first().likes.count(), 0)
