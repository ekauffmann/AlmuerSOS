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

from .views import CommentViewSet, ProductViewSet, RatingViewSet, StoreViewSet


router = routers.SimpleRouter()

router.register(r'stores', StoreViewSet, 'Store')
stores_router = routers.NestedSimpleRouter(router, r'stores', lookup='store')
stores_router.register(r'products', ProductViewSet, 'Product')
stores_router.register(r'ratings', RatingViewSet, 'Rating')
stores_router.register(r'comments', CommentViewSet, 'Comment')

urlpatterns = [
    url(r'^0/', include(router.urls)),
    url(r'^0/', include(stores_router.urls)),
]
