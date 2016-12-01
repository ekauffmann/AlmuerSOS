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

        users = self.client.get('/0/users/').json()

        self.assertEqual(1, len(users))
        self.assertEqual('test_user@test_user.com', users[0]['email'])

    def test_user_not_logged_in(self):
        users = self.client.get('/0/users/').json()

        self.assertEqual(0, len(users))
