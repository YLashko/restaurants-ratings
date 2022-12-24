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


def get_homepage_restaurants(request):
    content = '' if request.GET.get('search_for') is None else request.GET.get('search_for')
    items_num = int(request.GET.get("items_on_page"))

    cuisine_id = request.GET.get("cuisine")
    if cuisine_id not in [None, ""]:
        cuisine = RestaurantCuisine.objects.get(id=cuisine_id)
    else:
        cuisine = None

    profile_id = request.GET.get("profile")
    if profile_id not in [None, ""]:
        profile = Profile.objects.get(id=profile_id)
    else:
        profile = None
    restaurants = get_popular_restaurants(
        from_=items_num,
        cuisine=cuisine,
        search_for=content,
        profile=profile
    )
    return restaurants


def get_reviews(restaurant_id):
    return Review.objects.filter(restaurant_id=restaurant_id)


def get_profile(profile_id: str):
    return Profile.objects.get(id=profile_id)


def get_restaurant(restaurant_id: str):
    return Restaurant.objects.get(id=restaurant_id)


def get_cuisines():
    return RestaurantCuisine.objects.all()


def get_cuisines_for_recommendations_page(profile):
    return profile.profilecuisinestatistics_set.order_by(
        "-score"
    )[:3]


def get_review(review_id):
    return Review.objects.get(id=review_id)


def user_exists(username: str):
    return User.objects.filter(username=username).exists()


def user_can_edit_profile(user: User, profile: Profile):
    if user.profile != profile:
        raise PermissionError(_('You cannot edit this profile'))


def user_can_edit_restaurant(user: User, restaurant: Restaurant):
    if restaurant.profile.user != user:
        raise PermissionError(_('You cannot edit this restaurant'))


def user_can_review_restaurant(user: User, restaurant: Restaurant):
    if restaurant.profile.user == user:
        raise PermissionError(_('You cannot review your own restaurant'))
    if Review.objects.filter(profile=user.profile, restaurant=restaurant).exists():
        raise PermissionError(_('You have already reviewed this restaurant'))


def user_can_delete_review(user: User, review: Review):
    if review.profile.user != user:
        raise PermissionError(_('You cannot delete this review'))
