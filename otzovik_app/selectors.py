from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count, Q
from .config import ITEMS_PER_PAGE
from .models import *
from django.utils.translation import gettext as _


def get_popular_restaurants(from_: int | None, cuisine: str | None, search_for: str | None, company: str | None):
    restaurants = Restaurant.objects.filter(Q(name__icontains=search_for) |
                                            Q(description__icontains=search_for)).annotate(
        reviews_num=Count("review")
    ).order_by("-reviews_num", "-reviewsummary__rating")
    if cuisine is not None:
        restaurants = restaurants.filter(cuisines__cuisine__icontains=cuisine)
    if company is not None:
        restaurants = restaurants.filter(company_profile=company)
    restaurants = restaurants[from_: from_ + ITEMS_PER_PAGE]
    return restaurants


def get_company_profile(request, company_profile_id):
    return CompanyProfile.objects.get(id=company_profile_id)


def get_homepage_restaurants(request):
    content = '' if request.GET.get('search_for') is None else request.GET.get('search_for')
    items_num = int(request.GET.get("items_on_page"))

    cuisine_id = request.GET.get("cuisine")
    if cuisine_id not in [None, ""]:
        cuisine = RestaurantCuisine.objects.get(id=cuisine_id)
    else:
        cuisine = None

    company_id = request.GET.get("company_id")
    if company_id not in [None, ""]:
        company = CompanyProfile.objects.get(id=company_id)
    else:
        company = None
    restaurants = get_popular_restaurants(
        from_=items_num,
        cuisine=cuisine,
        search_for=content,
        company=company
    )
    return restaurants


def user_cuisines_for_recommendations(user_id):
    if len(get_user_reviews(user_id)) <= 3:
        return None
    user = User.objects.get(id=user_id)
    user_cuisines = user.profile.profilecuisinestatistics_set.order_by(
        "-score"
    )[:3]
    return user_cuisines


def get_reviews(restaurant_id: str):
    return Review.objects.filter(restaurant_id=restaurant_id)


def get_user_reviews(user_id: str):
    return Review.objects.filter(profile__user_id=user_id)


def get_profile(profile_id: str):
    return Profile.objects.get(id=profile_id)


def get_cities():
    return City.objects.all()


def get_city(name: str):
    return City.objects.get(name=name)


def get_all_food_types():
    return RestaurantFoodType.objects.all()


def get_all_prices():
    return RestaurantPrice.objects.all()


def get_food_type(food_type_id):
    return RestaurantFoodType.objects.get(id=food_type_id)


def get_price(price_id):
    return RestaurantPrice.objects.get(id=price_id)


def get_restaurant(restaurant_id: str):
    return Restaurant.objects.get(id=restaurant_id)


def get_cuisines():
    return RestaurantCuisine.objects.all()


def get_review(review_id):
    return Review.objects.get(id=review_id)


def user_exists(username: str):
    return User.objects.filter(username=username).exists()


def user_can_edit_profile(user: User, profile: Profile):
    if user.profile != profile:
        raise PermissionError(_('You cannot edit this profile'))


def user_can_edit_restaurant(user: User, restaurant: Restaurant):
    if restaurant.company_profile.profile.user != user:
        raise PermissionError(_('You cannot edit this restaurant'))


def user_can_review_restaurant(user: User, restaurant: Restaurant):
    if restaurant.company_profile.profile.user == user:
        raise PermissionError(_('You cannot review your own restaurant'))
    if Review.objects.filter(profile=user.profile, restaurant=restaurant).exists():
        raise PermissionError(_('You have already reviewed this restaurant'))


def user_can_create_company_profile(user: User):
    if CompanyProfile.objects.filter(profile__user=user).exists():
        raise PermissionError(_('You cannot create new company profile: you\'ve already created one'))


def user_can_edit_company_profile(user: User, company_profile: CompanyProfile):
    if not CompanyProfile.objects.filter(profile__user=user).exists():
        raise PermissionError(_('You cannot edit this company profile'))
    if user.profile.company_profile != company_profile:
        raise PermissionError(_('You cannot edit this company profile'))


def user_can_create_restaurant(user):
    if not CompanyProfile.objects.filter(profile__user=user).exists():
        raise PermissionError(_('To create restaurant, you must create company profile first'))


def user_can_delete_review(user: User, review: Review):
    if review.profile.user != user:
        raise PermissionError(_('You cannot delete this review'))
