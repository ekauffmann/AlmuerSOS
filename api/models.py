from django.contrib.auth.models import User
from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=12)
    managers = models.ManyToManyField(User)
    payment_methods = models.ManyToManyField('PaymentMethod')
    description = models.TextField()


class PaymentMethod(models.Model):
    name = models.CharField(max_length=128)


class Rating(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField()


class Product(models.Model):
    name = models.CharField(max_length=128)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


class ServiceDay(models.Model):
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    supply = models.IntegerField()
