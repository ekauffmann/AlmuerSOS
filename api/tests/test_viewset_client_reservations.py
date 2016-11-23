from django.contrib.auth.models import User
from django.test import TransactionTestCase
from rest_framework.test import APIClient


class ClientReservationViewSetTestCase(TransactionTestCase):
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
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user=user)

        reservations = self.client.get(
            '/0/users/{0:d}/reservations/'.format(user.pk)
        ).json()

        self.assertEqual(2, len(reservations))
        self.assertEqual('Lunchbox', reservations[0]['service_day']['product']['name'])
        self.assertEqual('Mongoliana', reservations[1]['service_day']['product']['name'])
