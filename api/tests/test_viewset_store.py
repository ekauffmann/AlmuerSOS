from django.test import TransactionTestCase
from rest_framework.test import APIClient


class StoreViewSetTestCase(TransactionTestCase):
    fixtures = [
        'test_stores.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def test_list_stores(self):
        stores = self.client.get('/0/stores/').json()

        self.assertEqual(2, len(stores))
        self.assertEqual('Chino', stores[1]['name'])
