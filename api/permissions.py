from rest_framework import permissions

from api.models import Store


def has_user_store_admin_permission(request, view, store_id_key):
    if request.method in ['GET', 'OPTIONS']:
        return True

    store_id = view.kwargs.get(store_id_key)

    if store_id is None:
        return False

    stores = Store.objects.filter(pk=store_id)

    if len(stores) is 0:
        return False

    return request.user.is_superuser or request.user in stores[0].managers.all()


class StoreManagerPermission(permissions.BasePermission):

    message = 'Solo los administradores pueden administrar esta tienda.'

    def has_permission(self, request, view):
        return has_user_store_admin_permission(request, view, 'pk')


class StoreNestedManagerPermission(permissions.BasePermission):

    message = 'Solo los administradores pueden administrar esta tienda.'

    def has_permission(self, request, view):
        return has_user_store_admin_permission(request, view, 'store_pk')
