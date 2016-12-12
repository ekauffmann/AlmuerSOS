"""almuersos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from rest_framework_nested import routers

from .views.comment import CommentViewSet
from .views.product import ProductViewSet
from .views.rating import RatingViewSet
from .views.reservation import ReservationViewSet
from .views.service_day import ServiceDayViewSet
from .views.store import StoreViewSet
from .views.user import UserReservationViewSet, UserViewSet, UserSessionViewSet


router = routers.SimpleRouter()

router.register(r'stores', StoreViewSet, 'Store')
stores_router = routers.NestedSimpleRouter(router, r'stores', lookup='store')
stores_router.register(r'products', ProductViewSet, 'Product')
stores_router.register(r'ratings', RatingViewSet, 'Rating')
stores_router.register(r'comments', CommentViewSet, 'Comment')
stores_router.register(r'reservations', ReservationViewSet, 'Reservation')
stores_router.register(r'service_days', ServiceDayViewSet, 'ServiceDay')

router.register(r'users', UserViewSet, 'User')
users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'reservations', UserReservationViewSet, 'UserReservation')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'', include(stores_router.urls)),
    url(r'', include(users_router.urls)),
    url(r'sessions', UserSessionViewSet.as_view({'get': 'list', 'delete': 'destroy'})),
]
