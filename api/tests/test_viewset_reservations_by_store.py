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

        self.base_data = {
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
            'user': {
                'id': 2,
            },
        }

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

    def test_client_reservations_without_login(self):
        reservations = self.client.get('/0/stores/1/reservations/').json()
        self.assertEqual(0, len(reservations))

    def test_create_reservation(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user=user)

        response = self.client.post(
            '/0/stores/1/reservations/',
            data=self.base_data,
            format='json'
        )

        self.assertEqual(200, response.status_code)

    def test_create_reservation_invalid_service_day(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user=user)

        data = self.base_data
        data['service_day']['date'] = '2011-01-01'

        response = self.client.post(
            '/0/stores/1/reservations/',
            data=data,
            format='json'
        )

        response_data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertEqual('No existe fecha de atención para este producto.', response_data['service_day'][0])

    def test_create_reservation_invalid_product(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user=user)

        data = self.base_data
        data['service_day']['product']['id'] = 9999

        response = self.client.post(
            '/0/stores/1/reservations/',
            data=data,
            format='json'
        )

        response_data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertEqual('El producto no existe.', response_data['service_day'][0])

    def test_create_reservation_invalid_user(self):
        user = User.objects.get(pk=2)
        self.client.force_authenticate(user=user)

        data = self.base_data
        data['user']['id'] = 9999

        response = self.client.post(
            '/0/stores/1/reservations/',
            data=data,
            format='json'
        )

        response_data = response.json()

        self.assertEqual('El usuario no existe.', response_data['user'][0])

    def test_create_reservation_user_is_store_manager(self):
        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)

        data = self.base_data
        data['user']['id'] = 1

        response = self.client.post(
            '/0/stores/1/reservations/',
            data=self.base_data,
            format='json'
        )

        response_data = response.json()

        self.assertEqual('El manager de esta tienda no puede reservar en su propia tienda.', response_data['user'][0])

    def test_create_reservation_invalid_demand(self):
        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)

        data = self.base_data
        data['demand'] = 0

        response = self.client.post(
            '/0/stores/1/reservations/',
            data=self.base_data,
            format='json'
        )

        response_data = response.json()

        self.assertEqual('No se puede reservar esa cantidad.', response_data['demand'][0])
