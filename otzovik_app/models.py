from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    unp = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class RestaurantCuisine(models.Model):
    cuisine = models.CharField(max_length=200)

    def __str__(self):
        return self.cuisine


class Restaurant(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=False, blank=False)
    short_description = models.TextField(max_length=625, null=False, blank=False, default='')
    cuisines = models.ManyToManyField(RestaurantCuisine, related_name='restaurant')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ReviewSummary(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, null=True)
    food_quality = models.FloatField(null=False, default=0)
    staff_quality = models.FloatField(null=False, default=0)
    price = models.FloatField(null=False, default=0)
    rating = models.FloatField(null=False, default=0)


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    food_quality = models.IntegerField(null=False, default=1)
    staff_quality = models.IntegerField(null=False, default=1)
    price = models.IntegerField(null=False, default=1)
    body = models.TextField(max_length=1000)

    def __str__(self):
        return f'Отзыв пользователя @{self.profile.user.username} на {self.restaurant.name}'


class PreviewImage(models.Model):
    preview_image = ResizedImageField(size=[640, 360], crop=['middle', 'center'], null=False, blank=False,
                                      upload_to='preview_images', default='grey.jpg')
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)


class AddressForGoogle(models.Model):
    lat = models.FloatField(null=False, blank=False)
    lng = models.FloatField(null=False, blank=False)
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)


class Address(models.Model):
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    building = models.CharField(max_length=30)
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
