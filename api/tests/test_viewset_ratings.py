from django.test import TransactionTestCase
from rest_framework.test import APIClient


class RatingViewSetTestCase(TransactionTestCase):
    fixtures = [
        'test_users.json',
        'test_stores.json',
        'test_ratings.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def test_list_ratings(self):
        ratings = self.client.get('/0/stores/1/ratings/').json()

        self.assertEqual(1, len(ratings))
        self.assertEqual(1, ratings[0]['value'])
