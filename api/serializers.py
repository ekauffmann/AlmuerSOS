# coding=utf-8
from django.contrib.auth.models import User
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Comment, PaymentMethod, Product, Rating, Reservation, ServiceDay, Store, StoreImage


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'store', 'user', 'date', 'text',)


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('id', 'name',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'value', 'store', 'user', 'date',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',)


class ServiceDaySerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ServiceDay
        fields = ('id', 'date', 'product', 'price', 'supply',)


class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    service_day = ServiceDaySerializer()

    class Meta:
        model = Reservation
        fields = ('id', 'user', 'service_day', 'demand',)

    def _get_product(self):
        products = Product.objects.filter(pk=self.initial_data['service_day']['product']['id'])

        if len(products) is not 1:
            raise serializers.ValidationError('El producto no existe.')

        return products[0]

    def validate_service_day(self, service_day):
        product = self._get_product()

        service_days = ServiceDay.objects.filter(
            product=product,
            date=service_day['date'],
        )

        if len(service_days) is not 1:
            raise serializers.ValidationError('No existe fecha de atención para este producto.')

        return service_days[0]

    def validate_user(self, user):
        product = self._get_product()

        users = User.objects.filter(pk=self.initial_data['user']['id'])

        if len(users) is not 1:
            raise serializers.ValidationError('El usuario no existe.')

        if users[0] in product.store.managers.all():
            raise serializers.ValidationError('El manager de esta tienda no puede reservar en su propia tienda.')

        return users[0]

    def validate_demand(self, demand):
        if int(demand) < 1:
            raise serializers.ValidationError('No se puede reservar esa cantidad.')

        return demand


class StoreSerializer(serializers.ModelSerializer):
    managers = UserSerializer(many=True, read_only=True)
    payment_methods = PaymentMethodSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ('id', 'name', 'phone', 'managers', 'payment_methods', 'description',)


class StoreImageSerializer(serializers.ModelSerializer):

    file = Base64ImageField()

    class Meta:
        model = StoreImage
        fields = ('id', 'store', 'file',)

    def create(self, validated_data):
        StoreImage.objects.filter(store=validated_data['store']).delete()
        return StoreImage.objects.create(**validated_data)
