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

    def test_get_product(self):
        products = self.client.get('/0/stores/1/products/1/').json()

        self.assertEqual('Lunchbox', products['name'])
