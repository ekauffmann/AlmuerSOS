from django.contrib.auth.models import User
from django.test import TransactionTestCase
from rest_framework.test import APIClient


class UserSessionViewSetTestCase(TransactionTestCase):
    fixtures = [
        'test_users.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def test_user_logged_in(self):
        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)

        session = self.client.get('/0/sessions/').json()

        self.assertEqual(dict, type(session))
        self.assertEqual('test_user@test_user.com', session['email'])

    def test_user_not_logged_in(self):
        session = self.client.get('/0/sessions/').json()

        self.assertEqual({}, session)

    def test_user_logout(self):
        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)

        session = self.client.get('/0/sessions/').json()

        self.assertEqual(dict, type(session))
        self.assertEqual('test_user@test_user.com', session['email'])

        session = self.client.delete('/0/sessions/').json()

        self.assertEqual({}, session)
