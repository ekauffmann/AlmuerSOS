from django.test import TransactionTestCase
from rest_framework.test import APIClient


class RatingViewSetTestCase(TransactionTestCase):
    fixtures = [
        'test_stores.json',
        'test_products.json',
        'test_service_days.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def test_list_service_days(self):
        service_days = self.client.get('/0/stores/1/service_days/?date=2016-05-16').json()

        self.assertEqual(1, len(service_days))
        self.assertEqual(1, service_days[0]['product']['id'])

    def test_get_rating(self):
        service_days = self.client.get('/0/stores/1/service_days/').json()

        self.assertEqual(0, len(service_days))
