from rest_framework import viewsets

from ..models import Store
from ..serializers import StoreSerializer


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
