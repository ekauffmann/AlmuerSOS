from django.test import TransactionTestCase
from rest_framework.test import APIClient


class CommentViewSetTestCase(TransactionTestCase):
    fixtures = [
        'test_users.json',
        'test_stores.json',
        'test_products.json',
        'test_service_days.json',
        'test_reservations.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def test_list_comments(self):
        reservations = self.client.get('/0/stores/2/reservations').json()

        self.assertEqual(1, len(reservations))
        self.assertEqual('Lunchbox', reservations[0]['product'])
