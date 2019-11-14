from django.contrib.auth.hashers import make_password
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

TEST_EMAIL = 'test@test.test'
TEST_PASS = 'pa55word'

TEST_EMAIL_2ND = 'test@test.testo'
TEST_PASS_2ND = 'pa55wordo'

BROKEN_TOKEN = 'abc'


class AccountsTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email=TEST_EMAIL,
                                        password=make_password(TEST_PASS))

        self.token = self.get_token(self.user.email, TEST_PASS)

    def get_token(self, email, password):
        url = reverse('token_obtain_pair')
        data = {
            'email': email,
            'password': password
        }
        response = self.client.post(url, data)

        token = response.data.get('access')
        return token

    def test_accounts_get_access_token(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': TEST_EMAIL,
            'password': TEST_PASS
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_accounts_create_user(self):
        url = reverse('users-list')
        data = {
            'email': TEST_EMAIL,
            'password': TEST_PASS
        }
        self.user.delete()
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, TEST_EMAIL)

    def test_accounts_get_user(self):
        url = reverse('users-detail', args=[self.user.id])

        response = self.client.get(
            url, HTTP_AUTHORIZATION='Bearer {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accounts_update_user(self):
        url = reverse('users-detail', args=[self.user.id])
        data = {'email': TEST_EMAIL_2ND}

        response = self.client.patch(
            url, data, HTTP_AUTHORIZATION='Bearer {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, TEST_EMAIL_2ND)

    def test_accounts_delete_user(self):
        url = reverse('users-detail', args=[self.user.id])

        response = self.client.delete(
            url, HTTP_AUTHORIZATION='Bearer {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_accounts_list_users(self):
        url = reverse('users-list')

        response = self.client.get(
            url, HTTP_AUTHORIZATION='Bearer {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, response.data[0]['email'])

    def test_accounts_list_users_broken_token(self):
        url = reverse('users-list')
        response = self.client.get(
            url, HTTP_AUTHORIZATION='Bearer {}'.format(BROKEN_TOKEN))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_accounts_list_users_unauthorized(self):
        url = reverse('users-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
