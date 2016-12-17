from rest_framework import viewsets

from ..models import Store, StoreImage
from ..permissions import StoreManagerPermission, StoreNestedManagerPermission
from ..serializers import StoreSerializer, StoreImageSerializer


class StoreViewSet(viewsets.ModelViewSet):
    permission_classes = (StoreManagerPermission,)

    serializer_class = StoreSerializer
    queryset = Store.objects.all()


class StoreImagesViewSet(viewsets.ModelViewSet):
    permission_classes = (StoreNestedManagerPermission,)

    serializer_class = StoreImageSerializer

    def get_queryset(self):
        params = {
            'store': self.kwargs['store_pk'],
        }

        image_id = self.kwargs.get('pk')

        if image_id is not None:
            params['pk'] = image_id

        return StoreImage.objects.filter(**params)
