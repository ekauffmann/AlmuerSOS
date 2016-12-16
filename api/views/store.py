from rest_framework import viewsets

from api.permissions import StoreManagerPermission
from ..models import Store
from ..serializers import StoreSerializer


class StoreViewSet(viewsets.ModelViewSet):
    permission_classes = (StoreManagerPermission,)

    serializer_class = StoreSerializer
    queryset = Store.objects.all()
