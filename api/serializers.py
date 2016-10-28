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


class ReservationSerializer(serializers.Serializer):
    date = serializers.DateField()
    product = ProductSerializer()
    supply = serializers.IntegerField()


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'phone', 'managers', 'payment_methods', 'description',)
