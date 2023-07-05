from django.core.handlers.wsgi import WSGIRequest
from django.utils.translation import gettext as _
from .forms import RestaurantForm, AddressForm, PreviewImageForm, UserForm, \
    ProfileForm, CoordinatesForm, ReviewForm, CompanyProfileForm, CityForm
from django.contrib.auth.password_validation import ValidationError
from .models import *
from .selectors import get_profile, user_can_edit_restaurant, get_restaurant, user_can_edit_profile, \
    user_can_review_restaurant, get_review, user_can_delete_review, get_company_profile, user_can_edit_company_profile, \
    user_can_create_restaurant, user_can_create_company_profile, get_city, get_price, get_food_type
from .util import collect_forms_errors


def create_cuisines_statistics(profile):  # refactor
    stats = ProfileCuisineStatistics.objects.filter(profile=profile)
    if len(stats) == 0:
        for cuisine in list(RestaurantCuisine.objects.all()):
            ProfileCuisineStatistics.objects.create(
                profile=profile,
                cuisine=cuisine
            )
    stats = ProfileCuisineStatistics.objects.filter(profile=profile)
    for cuisine in list(RestaurantCuisine.objects.all()):
        try:
            stat = stats.get(cuisine=cuisine)
            stat.score = len(list(Review.objects.filter(profile=profile,
                                                        restaurant__cuisines__cuisine__icontains=cuisine.cuisine)))
            stat.save()
        except:
            pass


def calculate_summary(restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant)
    summary = ReviewSummary.objects.get(restaurant=restaurant)
    if len(list(reviews)) > 0:
        fc = list(reviews.values_list('food_quality', flat=True))
        sc = list(reviews.values_list('staff_quality', flat=True))
        pr = list(reviews.values_list('price', flat=True))
        summary.food_quality = round(sum(fc) / len(fc), 1)
        summary.staff_quality = round(sum(sc) / len(sc), 1)
        summary.price = round(sum(pr) / len(pr), 1)
        summary.rating = round(sum([summary.food_quality, summary.staff_quality, summary.price]) / 3, 1)
    else:
        summary.food_quality = 0
        summary.staff_quality = 0
        summary.price = 0
        summary.rating = 0
    summary.save()


def register_user(request: WSGIRequest):
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)
    city = get_city(request.POST.get("city"))

    if user_form.is_valid():
        user = user_form.save(commit=False)

    if User.objects.filter(username=user_form.data.get("username")).exists():
        raise ValueError(_('User already exists'))

    if Profile.objects.filter(email=profile_form.data.get("email")).exists():
        raise ValueError(_('Email already taken'))

    if user_form.is_valid() and profile_form.is_valid():
        user.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.city = city
        profile.save()
        return user
    else:
        raise ValueError(collect_forms_errors([user_form, profile_form]))


def save_profile(request: WSGIRequest, profile_id):
    profile_form = ProfileForm(request.POST, instance=get_profile(profile_id))
    city = get_city(request.POST.get("city"))
    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        profile.city = city
        profile.save()
    else:
        raise ValueError(str(profile_form.errors))


def create_restaurant(request: WSGIRequest):
    user_can_create_restaurant(request.user)
    restaurant_form = RestaurantForm(request.POST)
    address_form = AddressForm(request.POST)
    coordinates_form = CoordinatesForm(request.POST)
    if all([restaurant_form.is_valid(),
            address_form.is_valid(),
            coordinates_form.is_valid()]):

        restaurant = restaurant_form.save(commit=False)
        address = address_form.save(commit=False)
        coordinates = coordinates_form.save(commit=False)

        address.restaurant = restaurant
        coordinates.restaurant = restaurant

        restaurant.company = request.user.profile.company_profile
        restaurant.price = get_price(request.POST.get("price"))
        restaurant.food_type = get_food_type(request.POST.get("food_type"))
        address.city = get_city(request.POST.get("city"))

        address.save()
        coordinates.save()
        restaurant.save()

        ReviewSummary.objects.create(
            restaurant=restaurant
        )

        cuisines = request.POST.getlist("cuisines")[:3]
        for cuisine in cuisines:
            restaurant.cuisines.add(RestaurantCuisine.objects.get(id=cuisine))

        preview_image_form = PreviewImageForm(request.POST, request.FILES)
        if preview_image_form.is_valid():
            image_form = preview_image_form.save(commit=False)
            image_form.restaurant = restaurant
            image_form.save()

        images = request.FILES.getlist("images")
        for image in images:
            created_image = RestaurantImage.objects.create(image=image, restaurant=restaurant)
            created_image.save()
    else:
        raise ValueError(collect_forms_errors([restaurant_form, address_form, coordinates_form]))


def create_company_profile(request: WSGIRequest):
    user_can_create_company_profile(request.user)
    company_profile_form = CompanyProfileForm(request.POST)
    address_form = AddressForm(request.POST)
    if all([company_profile_form.is_valid(), address_form.is_valid()]):
        address = address_form.save(commit=False)
        company_profile = company_profile_form.save(commit=False)
        company_profile.address = address
        company_profile.profile = request.user.profile
        address.city = get_city(request.POST.get("city"))
        address.save()
        company_profile.save()
    else:
        raise ValueError(collect_forms_errors([address_form, company_profile_form]))


def save_restaurant(request: WSGIRequest, restaurant_id):
    restaurant = get_restaurant(restaurant_id)
    user_can_edit_restaurant(request.user, restaurant)

    restaurant_form = RestaurantForm(request.POST, instance=restaurant)
    address_form = AddressForm(request.POST, instance=restaurant.address)
    coordinates_form = CoordinatesForm(request.POST, instance=restaurant.coordinates)

    if all([restaurant_form.is_valid(),
            address_form.is_valid(),
            coordinates_form.is_valid()]):
        restaurant = restaurant_form.save(commit=False)
        restaurant.price = get_price(request.POST.get("price"))
        restaurant.food_type = get_food_type(request.POST.get("food_type"))
        address = address_form.save(commit=False)
        address.city = get_city(request.POST.get("city"))
        address.save()
        coordinates_form.save()
        restaurant.save()
    else:
        raise ValidationError(collect_forms_errors([restaurant_form, address_form, coordinates_form]))


def save_company_profile(request, company_profile_id):
    company_profile = get_company_profile(request, company_profile_id)
    user_can_edit_company_profile(request.user, company_profile)
    city = get_city(request.POST.get("city"))
    company_profile_form = CompanyProfileForm(request.POST, instance=company_profile)
    company_profile = company_profile_form.save()
    address_form = AddressForm(request.POST, instance=company_profile.address)

    if all([company_profile_form.is_valid(), address_form.is_valid()]):
        address = address_form.save(commit=False)
        address.city = city
        address.save()
    else:
        raise ValueError(collect_forms_errors([company_profile_form, address_form]))


def set_unp(request, profile_id):
    profile = get_profile(profile_id)
    user_can_edit_profile(request.user, profile)
    profile.unp = request.POST.get('unp')
    profile.save()


def create_review(request, restaurant_id):
    restaurant = get_restaurant(restaurant_id)
    user_can_review_restaurant(request.user, restaurant)

    review_form = ReviewForm(request.POST)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.restaurant = restaurant
        review.profile = request.user.profile
        review.save()
    else:
        raise ValueError(collect_forms_errors([review_form]))

    calculate_summary(restaurant.id)
    create_cuisines_statistics(request.user.profile)


def delete_review_service(request, review_id):
    review = get_review(review_id)
    user_can_delete_review(request.user, review)
    restaurant_id = review.restaurant.id
    review.delete()
    calculate_summary(restaurant_id)
