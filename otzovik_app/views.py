from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password, ValidationError
from .models import *
from .services import register_user, save_profile, create_restaurant, \
    save_restaurant, set_unp, create_review, delete_review_service
from .selectors import get_popular_restaurants, get_profile, user_can_edit_profile, user_exists, get_restaurant, \
    user_can_edit_restaurant, get_cuisines, get_review, get_cuisines_for_recommendations_page, get_homepage_restaurants, \
    get_reviews
from .config import REVIEWS_PER_PAGE


def home_page(request):
    search_for = '' if request.GET.get('search_for') is None else request.GET.get('search_for')

    cuisines = RestaurantCuisine.objects.all()  # refactor

    restaurants = get_popular_restaurants(
        from_=0,
        cuisine=None,
        search_for=search_for,
        profile=None
    )

    context = {'content': search_for, 'restaurants': restaurants, "cuisines": cuisines}
    return render(request, 'otzovik_app/home.html', context)


def registration_page(request):
    context = {
        'type': 'register',
        'name': request.POST.get('name') if request.POST.get('name') else '',
        'surname': request.POST.get('surname') if request.POST.get('surname') else '',
        'email': request.POST.get('email') if request.POST.get('email') else '',
        'username': request.POST.get('username') if request.POST.get('username') else ''
    }

    if request.method == 'POST':
        try:
            user = register_user(request)
            login(request, user)
            return redirect('home')
        except ValueError as msg:
            messages.error(request, msg)

    return render(request, 'otzovik_app/registration_page.html', context)


@login_required(login_url='login_page')
def edit_profile(request, pk):
    profile = get_profile(pk)
    context = {'type': 'edit', 'profile': profile}
    try:
        user_can_edit_profile(request.user, profile)
    except PermissionError as msg:
        messages.error(request, msg)
        return redirect('home')

    if request.method == 'POST':
        try:
            save_profile(request, pk)
            return redirect('user_profile', pk)
        except ValueError as msg:
            messages.error(request, msg)
            return render(request, 'otzovik_app/registration_page.html', context)
        except PermissionError as msg:
            messages.error(request, msg)
            return redirect('home')

    return render(request, 'otzovik_app/registration_page.html', context)


def login_page(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')

        if not user_exists(username):
            messages.error(request, f'User {username} does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, _('Password is incorrect'))
    return render(request, 'otzovik_app/login_page.html', context)


@login_required(login_url='login_page')
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url="login_page")
def edit_restaurant(request, pk):
    restaurant = get_restaurant(pk)
    try:
        user_can_edit_restaurant(request.user, restaurant)
    except PermissionError as msg:
        messages.error(request, msg)
        return redirect("restaurant_main", restaurant.id)

    if request.method == "POST":
        try:
            save_restaurant(request, pk)
        except ValidationError as msg:
            messages.error(request, msg)
        except PermissionError as msg:
            messages.error(request, msg)
        return redirect("restaurant_main", restaurant.id)

    cuisines = RestaurantCuisine.objects.all()
    context = {"restaurant": restaurant, "cuisines": cuisines, "type": "edit"}
    return render(request, "otzovik_app/new_restaurant.html", context)


@login_required(login_url='login_page')
def new_restaurant(request):
    if request.method == "POST":
        try:
            create_restaurant(request)
        except ValueError as msg:
            messages.error(request, msg)
        return redirect('home')
    cuisines = get_cuisines()
    cuisines_names = [cuisine.cuisine for cuisine in cuisines]
    context = {
        "cuisines": cuisines,
        "cuisines_list": cuisines_names,
        "type": "register"
    }
    return render(request, 'otzovik_app/new_restaurant.html', context)


@login_required(login_url='login_page')
def user_profile(request, pk):
    profile = get_profile(pk)
    context = {'profile': profile}
    if request.method == 'POST':
        try:
            set_unp(request, pk)
        except PermissionError as msg:
            messages.error(request, msg)
        return redirect('user_profile', profile.id)
    return render(request, 'otzovik_app/user_profile.html', context)


@login_required(login_url='login_page')
def delete_review(request, pk):
    review = get_review(pk)

    if request.method == 'POST':
        try:
            delete_review_service(request, pk)
        except PermissionError as msg:
            messages.error(request, msg)
        return redirect(request.GET.get('redirect'))

    context = {'object': review}
    return render(request, 'otzovik_app/delete_object.html', context)


@login_required(login_url="login_page")
def recommendations_page(request):
    profile = request.user.profile
    cuisines = get_cuisines_for_recommendations_page(profile)
    context = {
        "cuisines": cuisines,
    }
    return render(request, 'otzovik_app/recommendations_page.html', context)


def restaurant_main(request, pk):
    restaurant = get_restaurant(pk)
    context = {'restaurant': restaurant}
    return render(request, 'otzovik_app/restaurant_main.html', context)


@login_required(login_url='login_page')
def new_review(request, pk):
    restaurant = get_restaurant(pk)
    if request.method == "POST":
        try:
            create_review(request, pk)
        except ValueError as msg:
            messages.error(request, msg)
        except PermissionError as msg:
            messages.error(request, msg)
        return redirect('restaurant_main', restaurant.id)
    context = {'restaurant': restaurant}
    return render(request, 'otzovik_app/new_review.html', context)


def validate_username_ajax(request):
    exists = user_exists(request.POST.get('login'))
    response = {
        "is_taken": exists,
        "resp_message": _("This username is taken!") if exists else ""
    }
    return JsonResponse(response)


def validate_password_ajax(request):
    try:
        validate_password(request.GET.get("password1"))
        valid = True
        reason = _("This password is valid")
    except ValidationError as err:
        valid = False
        reason = " ".join(err.messages)

    response = {
        "is_valid": valid,
        "reason": reason
    }
    return JsonResponse(response)


def update_homepage_content(request):
    restaurants = get_homepage_restaurants(request)
    context = {"restaurants": restaurants}
    response = {"content": (render_to_string("otzovik_app/restaurants_feed_component.html", context, request))}
    return JsonResponse(response)


def get_reviews_ajax(request):
    restaurant_id = request.GET.get("restaurant_id")
    from_ = int(request.GET.get("start_from"))
    reviews = get_reviews(restaurant_id)[from_: from_ + REVIEWS_PER_PAGE]
    context = {"reviews": reviews}
    response = {"content": render_to_string("otzovik_app/reviews_component.html", context, request)}
    return JsonResponse(response)


@login_required(login_url="login_page")
def admin_page(request):
    if not Admin.objects.filter(profile=request.user.profile).exists():
        return render(request, "otzovik_app/you_are_not_supposed_to_be_here.html", {})
    context = {}
    return render(request, "otzovik_app/admin_main.html", context)
