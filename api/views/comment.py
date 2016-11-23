from rest_framework import viewsets

from ..models import Comment
from ..serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        params = {
            'store': self.kwargs.get('store_pk')
        }

        comment_id = self.kwargs.get('pk')

        if comment_id is not None:
            params['pk'] = comment_id

        return Comment.objects.filter(**params)
