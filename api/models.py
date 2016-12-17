import uuid

from django.contrib.auth.models import User
from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=12)
    managers = models.ManyToManyField(User)
    payment_methods = models.ManyToManyField('PaymentMethod')
    description = models.TextField()

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Rating(models.Model):
    LIKE = 1
    DISLIKE = -1
    CHOICES = (
        (LIKE, 'LIKE'),
        (DISLIKE, 'DISLIKE'),
    )

    value = models.IntegerField(choices=CHOICES)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()


class Comment(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.TextField()


class Product(models.Model):
    name = models.CharField(max_length=128)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    description = models.TextField(default=None, null=True)

    def __str__(self):
        return self.name


class ServiceDay(models.Model):
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    supply = models.IntegerField()


# sum of reservations must be leq than supply
class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_day = models.ForeignKey(ServiceDay, on_delete=models.CASCADE)
    demand = models.IntegerField()


class StoreImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='images_store', max_length=254)
