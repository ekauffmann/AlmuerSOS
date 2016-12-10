from django.contrib import admin

from .models import PaymentMethod, Product, Store


class StoreAdmin(admin.ModelAdmin):
    pass


class PaymentMethodAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(Store, StoreAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Product, ProductAdmin)
