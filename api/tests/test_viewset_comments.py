from django.test import TransactionTestCase
from rest_framework.test import APIClient


class CommentViewSetTestCase(TransactionTestCase):
    fixtures = [
        'test_users.json',
        'test_stores.json',
        'test_comments.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def test_list_comments(self):
        comments = self.client.get('/0/stores/2/comments/').json()

        self.assertEqual(1, len(comments))
        self.assertEqual('Ñe', comments[0]['text'])
