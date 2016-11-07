from django.contrib.auth.models import User
from django.test import TransactionTestCase
from rest_framework.test import APIClient
from ..views import ReservationViewSet


class ReservationViewSetTestCase(TransactionTestCase):
    fixtures = [
        'test_users.json',
        'test_stores.json',
        'test_products.json',
        'test_service_days.json',
        'test_reservations.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def test_list_reservations(self):
        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)

        reservations = self.client.get('/0/stores/1/reservations/').json()

        self.assertEqual(1, len(reservations))
        self.assertEqual('Lunchbox', reservations[0]['product']['name'])
