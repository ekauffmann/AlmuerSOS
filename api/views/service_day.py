from datetime import date

from rest_framework import viewsets

from ..models import ServiceDay
from ..serializers import ServiceDaySerializer


class ServiceDayViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceDaySerializer

    def get_queryset(self):
        date_ = self.request.GET.get('date')
        if date_ is None:
            date_ = date.today()

        params = {
            'product__store': self.kwargs['store_pk'],
            'date': date_
        }

        service_day_id = self.kwargs.get('pk')

        if service_day_id is not None:
            params['pk'] = service_day_id

        return ServiceDay.objects.filter(**params)
