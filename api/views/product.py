from rest_framework import viewsets

from ..models import Product
from ..serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        params = {
            'store': self.kwargs['store_pk']
        }

        product_id = self.kwargs.get('pk')

        if product_id is not None:
            params['pk'] = product_id

        return Product.objects.filter(**params)