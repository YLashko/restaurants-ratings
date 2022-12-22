from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count, Q
from .config import ITEMS_PER_PAGE
from .models import *
from django.utils.translation import gettext as _


def get_popular_restaurants(from_: int | None, cuisine: str | None, search_for: str | None, profile: str | None):
    restaurants = Restaurant.objects.filter(Q(name__icontains=search_for) |
                                            Q(description__icontains=search_for)).annotate(
        reviews_num=Count("review")
    ).order_by("-reviews_num", "-reviewsummary__rating")
    if cuisine is not None:
        restaurants = restaurants.filter(cuisines__cuisine__icontains=cuisine)
    if profile is not None:
        restaurants = restaurants.filter(profile=profile)
    restaurants = restaurants[from_: from_ + ITEMS_PER_PAGE]
    return restaurants


def get_profile(profile_id: str):
    return Profile.objects.get(id=profile_id)


def get_restaurant(restaurant_id: str):
    return Restaurant.objects.get(id=restaurant_id)


def user_exists(username: str):
    return User.objects.filter(username=username).exists()


def user_can_edit_profile(user: User, profile: Profile):
    if user.profile != profile:
        raise PermissionError(_('You cannot edit this profile'))


def user_can_edit_restaurant(user: User, restaurant: Restaurant):
    if restaurant.profile.user.id != user.id:
        raise PermissionError(_('You cannot edit this restaurant'))
