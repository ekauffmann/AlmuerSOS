from django.contrib.auth.models import User
from django.test import TransactionTestCase
from rest_framework.test import APIClient


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

    def test_manager_reservations(self):
        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)

        reservations = self.client.get('/0/stores/1/reservations/').json()

        self.assertEqual(1, len(reservations))
        self.assertEqual('Lunchbox', reservations[0]['service_day']['product']['name'])

    def test_client_reservations(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user=user)

        reservations = self.client.get('/0/stores/1/reservations/').json()

        self.assertEqual(1, len(reservations))
        self.assertEqual('Lunchbox', reservations[0]['service_day']['product']['name'])

        reservations = self.client.get('/0/stores/2/reservations/').json()

        self.assertEqual(1, len(reservations))
        self.assertEqual('Mongoliana', reservations[0]['service_day']['product']['name'])

    def test_create_user_reservation(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user=user)

        response = self.client.post(
            '/0/stores/1/reservations/',
            data={
                'service_day': {
                    'date': '2016-05-16',
                    'product': {
                        'id': 1,
                        'name': 'asdf',
                    },
                    'price': 1,
                    'supply': 2,
                },
                'demand': 1,
                'user': 2
            },
            format='json'
        )

        self.assertEqual(200, response.status_code)
