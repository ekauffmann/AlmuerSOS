from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Reservation, Store
from ..serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Reservation.objects.none()

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

        return reservations

    def create(self, request, store_pk, *a, **ka):
        serializer = ReservationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)
