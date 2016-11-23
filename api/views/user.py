from django.contrib.auth.models import User
from rest_framework import viewsets

from ..models import Reservation
from ..serializers import ReservationSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.none()


class UserReservationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        users = User.objects.filter(
            pk=self.kwargs.get('user_pk')
        )

        if len(users) is 0 \
                or (self.request.user.pk is not users[0].pk
                    and not self.request.user.is_superuser):
            return User.objects.none()

        return Reservation.objects.filter(user=users[0])
