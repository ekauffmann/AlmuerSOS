from django.test import TestCase

from ..apps import ApiConfig


class ClientReservationViewSetTestCase(TestCase):

    def test_app(self):
        self.assertEqual('api', ApiConfig.name)
