from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password, ValidationError
from .models import *
from .services import register_user, calculate_summary, create_cuisines_statistics, save_profile, create_restaurant, \
    save_restaurant
from .util import calculate_pages
from .selectors import get_popular_restaurants, get_profile, user_can_edit_profile, user_exists, get_restaurant, \
    user_can_edit_restaurant
from .config import ITEMS_PER_PAGE, REVIEWS_PER_PAGE


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
    cuisines = RestaurantCuisine.objects.all()
    cuisines_list = [cuisine.cuisine for cuisine in cuisines]
    context = {
        "cuisines": cuisines,
        "cuisines_list": cuisines_list,
        "type": "register"
    }
    return render(request, 'otzovik_app/new_restaurant.html', context)


@login_required(login_url='login_page')
def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile}
    if request.method == 'POST':
        profile.unp = request.POST.get('unp')
        profile.save()
        return redirect('user_profile', profile.id)
    return render(request, 'otzovik_app/user_profile.html', context)


@login_required(login_url='login_page')
def delete_review(request, pk):
    review = Review.objects.get(id=pk)

    if request.user != review.profile.user:
        return HttpResponse('Что-то пошло не так...')

    if request.method == 'POST':
        restaurant_id = review.restaurant.id
        review.delete()
        calculate_summary(restaurant_id)
        return redirect(request.GET.get('redirect'))

    context = {'object': review}
    return render(request, 'otzovik_app/delete_object.html', context)


@login_required(login_url="login_page")
def recommendations_page(request):
    profile = request.user.profile
    cuisines = profile.profilecuisinestatistics_set.order_by(
        "-score"
    )[:3]
    context = {
        "cuisines": cuisines,
    }
    return render(request, 'otzovik_app/recommendations_page.html', context)


def restaurant_main(request, pk):
    restaurant = Restaurant.objects.get(id=pk)
    reviews = Review.objects.filter(restaurant=restaurant).all()
    page = 0 if request.GET.get('page') in [None, "0", ""] else int(request.GET.get('page'))

    max_page = (len(reviews) - 1) // REVIEWS_PER_PAGE
    min_page = 0 if page > 0 else "NaN"
    prev_page = page - 1 if page > 0 else "NaN"
    next_page = page + 1 if page < max_page else "NaN"
    max_page = max_page if page < max_page else "NaN"

    context = {'restaurant': restaurant, 'reviews': reviews[page * REVIEWS_PER_PAGE: (page + 1) * REVIEWS_PER_PAGE],
               'page': page, 'max_page': max_page, 'prev_page': prev_page, 'next_page': next_page, 'min_page': min_page}
    return render(request, 'otzovik_app/restaurant_main.html', context)


@login_required(login_url='login_page')
def new_review(request, pk):
    restaurant = Restaurant.objects.get(id=pk)
    try:
        Review.objects.get(profile_id=request.user.profile.id, restaurant=restaurant)
        messages.error(request, _('You have already reviewed this restaurant!'))
        return redirect('restaurant_main', pk)
    except:
        pass
    if request.method == "POST":
        Review.objects.create(
            restaurant=restaurant,
            profile=request.user.profile,
            food_quality=request.POST.get("food_quality"),
            staff_quality=request.POST.get("staff_quality"),
            price=request.POST.get("price"),
            body=request.POST.get("body")
        )
        calculate_summary(restaurant.id)
        create_cuisines_statistics(request.user.profile)
        return redirect('restaurant_main', restaurant.id)

    context = {'restaurant': restaurant}
    return render(request, 'otzovik_app/new_review.html', context)


def validate_username(request):
    exists = Profile.objects.filter(user__username=request.GET.get("login")).exists()
    response = {
        "is_taken": exists,
        "resp_message": _("This username is taken!") if exists else ""
    }
    return JsonResponse(response)


def validate_password_ajax(request):
    try:
        validate_password(request.GET.get("password1"))
        valid = True
        reason = "This password is ok"
    except ValidationError as err:
        valid = False
        reason = " ".join(err.messages)

    response = {
        "is_valid": valid,
        "reason": reason
    }
    return JsonResponse(response)


def update_homepage_content(request):
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
    context = {"restaurants": restaurants}
    response = {"content": (render_to_string("otzovik_app/restaurants_feed_component.html", context, request))}
    return JsonResponse(response)


def get_reviews(request):
    restaurant_id = request.GET.get("restaurant_id")
    from_ = int(request.GET.get("start_from"))
    reviews = Review.objects.filter(restaurant_id=restaurant_id)[from_: from_ + REVIEWS_PER_PAGE]
    context = {"reviews": reviews}
    response = {"content": render_to_string("otzovik_app/reviews_component.html", context, request)}
    return JsonResponse(response)


@login_required(login_url="login_page")
def admin_page(request):
    if not Admin.objects.filter(profile=request.user.profile).exists():
        return render(request, "otzovik_app/you_are_not_supposed_to_be_here.html", {})
    context = {}
    return render(request, "otzovik_app/admin_main.html", context)
