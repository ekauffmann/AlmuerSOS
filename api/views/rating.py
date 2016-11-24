from rest_framework import viewsets

from ..models import Rating
from ..serializers import RatingSerializer


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer

    def get_queryset(self):
        params = {
            'store': self.kwargs['store_pk']
        }

        rating_id = self.kwargs.get('pk')

        if rating_id is not None:
            params['pk'] = rating_id

        return Rating.objects.filter(**params)
