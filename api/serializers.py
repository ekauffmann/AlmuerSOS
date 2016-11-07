from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment, Product, Rating, Store


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'store', 'user', 'date', 'text',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name',)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'value', 'store', 'user', 'date',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',)


class ReservationSerializer(serializers.Serializer):
    date = serializers.DateField()
    user = UserSerializer()
    product = ProductSerializer()
    demand = serializers.IntegerField()


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'phone', 'managers', 'payment_methods', 'description',)
