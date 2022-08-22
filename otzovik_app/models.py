from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class AddressForGoogle(models.Model):
    lat = models.FloatField(null=False, blank=False)
    lng = models.FloatField(null=False, blank=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class Address(models.Model):
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    building = models.CharField(max_length=30)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
