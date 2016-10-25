from django.test import TransactionTestCase
from rest_framework.test import APIClient


class ProductViewSetTestCase(TransactionTestCase):
    fixtures = [
        'test_stores.json',
        'test_products.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def test_list_products(self):
        products = self.client.get('/0/stores/1/products/').json()

        self.assertEqual(4, len(products))
        self.assertEqual('Lunchbox', products[0]['name'])
