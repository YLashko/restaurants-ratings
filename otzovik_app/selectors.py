from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count, Q
from .config import ITEMS_PER_PAGE
from .models import *


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
