from rest_framework import viewsets

from .models import Comment, Product, Rating, Reservation, Store
from .serializers import CommentSerializer, ProductSerializer, RatingSerializer, ReservationSerializer, StoreSerializer


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


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        params = {
            'store': self.kwargs.get('store_pk')
        }

        product_id = self.kwargs.get('pk')

        if product_id is not None:
            params['pk'] = product_id

        return Product.objects.filter(**params)


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer

    def get_queryset(self):
        params = {
            'store': self.kwargs.get('store_pk')
        }

        rating_id = self.kwargs.get('pk')

        if rating_id is not None:
            params['pk'] = rating_id

        return Rating.objects.filter(**params)


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Rating.objects.none()

        stores = Store.objects.filter(
            pk=self.kwargs.get('store_pk')
        )

        if self.request.user in stores[0].managers.all():
            reservations = Reservation.objects.filter(
                service_day__product__store=stores
            )

        else:
            reservations = Reservation.objects.filter(
                service_day__product__store=stores,
                user=self.request.user
            )

        return [
            {
                'date': r.service_day.date,
                'user': r.user,
                'product': r.service_day.product,
                'demand': r.demand
            } for r in reservations
        ]


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
