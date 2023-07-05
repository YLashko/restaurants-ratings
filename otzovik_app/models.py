from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class Coordinates(models.Model):
    lat = models.FloatField(null=False, blank=False)
    lng = models.FloatField(null=False, blank=False)


class City(models.Model):
    name = models.CharField(max_length=200)


class Address(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False)
    street = models.CharField(max_length=200)
    building = models.CharField(max_length=30)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    unp = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CompanyProfile(models.Model):
    profile = models.OneToOneField(Profile, related_name='company_profile', on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, blank=False)
    description = models.CharField(max_length=1000)
    nip = models.CharField(max_length=20)
    owner_name = models.CharField(max_length=50)
    owner_surname = models.CharField(max_length=50)


class Admin(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True)


class RestaurantCuisine(models.Model):
    cuisine = models.CharField(max_length=200)

    def __str__(self):
        return self.cuisine


class RestaurantPrice(models.Model):
    price = models.CharField(max_length=200)

    def __str__(self):
        return self.price


class RestaurantFoodType(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class ProfileCuisineStatistics(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)
    cuisine = models.ForeignKey(RestaurantCuisine, on_delete=models.CASCADE)
    score = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'{self.profile} - {self.cuisine} - {self.score}'


class Restaurant(models.Model):
    company_profile = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, blank=False, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=False, blank=False)
    short_description = models.TextField(max_length=625, null=False, blank=False, default='')
    cuisines = models.ManyToManyField(RestaurantCuisine, related_name='restaurant')
    price = models.ForeignKey(RestaurantPrice, related_name='restaurant', on_delete=models.SET_NULL, null=True)
    food_type = models.ForeignKey(RestaurantFoodType, related_name='restaurant', on_delete=models.SET_NULL, null=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, blank=False, null=True)
    coordinates = models.OneToOneField(Coordinates, on_delete=models.CASCADE, null=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ReviewSummary(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, blank=False)
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


class RestaurantImage(models.Model):
    image = ResizedImageField(size=[1920, 1080], crop=['middle', 'center'], null=False, blank=False,
                              upload_to='restaurant_images', default='grey.jpg')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
