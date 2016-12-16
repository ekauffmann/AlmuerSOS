import json

from rest_framework import permissions

from api.models import Store


class StoreManagerPermission(permissions.BasePermission):

    message = 'Solo los administradores pueden administrar esta tienda.'

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS']:
            return True

        stores = Store.objects.filter(pk=request.data['id'])

        if len(stores) is 0:
            return False

        return request.user.is_superuser or request.user in stores[0].managers.all()
