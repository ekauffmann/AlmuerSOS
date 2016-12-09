from django.contrib import admin

from .models import PaymentMethod, Store


class StoreAdmin(admin.ModelAdmin):
    pass


class PaymentMethodAdmin(admin.ModelAdmin):
    pass


admin.site.register(Store, StoreAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
