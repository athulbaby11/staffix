from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from admin_app.models import Job


class JobApiTests(APITestCase):
    def setUp(self):
        self.job = Job.objects.create(
            company_name='Example Care',
            job_title='Care worker',
            job_description='Support people in their homes.',
            location='London',
            salary='12',
            job_type='full_time',
            employment_type='permanent',
        )

    def test_job_list_is_public_and_returns_serialized_jobs(self):
        response = self.client.get('/api/v1/jobs/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['results'][0]['slug'], self.job.slug)
        self.assertEqual(response.data['results'][0]['company_name'], 'Example Care')

    def test_job_detail_is_public_and_uses_job_slug(self):
        response = self.client.get(f'/api/v1/jobs/{self.job.slug}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['job_title'], 'Care worker')

    def test_current_user_requires_a_valid_token(self):
        response = self.client.get('/api/v1/auth/me/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_login_and_current_user_endpoint(self):
        user = get_user_model().objects.create_user(
            username='flutter-admin',
            password='safe-test-password',
        )

        token_response = self.client.post('/api/v1/auth/token/', {
            'username': user.username,
            'password': 'safe-test-password',
        })

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertTrue(Token.objects.filter(key=token_response.data['token'], user=user).exists())

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token_response.data['token']}")
        user_response = self.client.get('/api/v1/auth/me/')

        self.assertEqual(user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_response.data, {'username': user.username})

    def test_token_login_rejects_invalid_password(self):
        user = get_user_model().objects.create_user(
            username='flutter-admin',
            password='safe-test-password',
        )

        response = self.client.post('/api/v1/auth/token/', {
            'username': user.username,
            'password': 'wrong-password',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
