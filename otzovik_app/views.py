from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from .forms import RestaurantForm, AddressForm, AddressForGoogleForm, PreviewImageForm, CuisineForm
from django.contrib.auth.password_validation import validate_password, ValidationError
from .models import *
from .util import calculate_summary, calculate_pages, get_popular_restaurants, create_cuisines_statistics
from .config import ITEMS_PER_PAGE, REVIEWS_PER_PAGE


def home_page(request):
    content = '' if request.GET.get('search_for') is None else request.GET.get('search_for')

    cuisines = RestaurantCuisine.objects.all()

    restaurants = get_popular_restaurants(
        from_=0,
        cuisine=None,
        search_for=content,
        profile=None
    )

    context = {'content': content, 'restaurants': restaurants, "cuisines": cuisines}
    return render(request, 'otzovik_app/home.html', context)


def registration_page(request):
    def fill_context_from_post():
        context['name'] = request.POST.get('name')
        context['surname'] = request.POST.get('surname')
        context['email'] = request.POST.get('email')
        context['login'] = request.POST.get('login')

    context = {'type': 'register'}
    if request.method == 'POST':

        try:
            validate_password(request.POST.get('password'))
        except ValidationError:
            messages.error(request, _("Try another password"))
            fill_context_from_post()
            return render(request, 'otzovik_app/registration_page.html', context)

        try:
            User.objects.get(username=request.POST.get("Username"))
            messages.error(request, _("Username already taken"))
            fill_context_from_post()
            return render(request, 'otzovik_app/registration_page.html', context)
        except:
            pass

        try:
            Profile.objects.get(email=request.POST.get('email'))
            messages.error(request, _("Email already taken"))
            fill_context_from_post()
            return render(request, 'otzovik_app/registration_page.html', context)
        except:
            pass

        user = User.objects.create(
            username=request.POST.get('login'),
            password=request.POST.get('password'),
        )
        Profile.objects.create(
            name=request.POST.get('name'),
            surname=request.POST.get('surname'),
            email=request.POST.get('email'),
            unp='',
            user=user,
        )
        login(request, user)
        return redirect('home')
    return render(request, 'otzovik_app/registration_page.html', context)


@login_required(login_url='login_page')
def edit_profile(request, pk):
    if request.method == 'POST':
        profile = Profile.objects.get(id=pk)
        if request.user == profile.user:
            profile.name = request.POST.get('name')
            profile.surname = request.POST.get('surname')
            profile.email = request.POST.get('email')
            profile.save()
            return redirect('user_profile', profile.id)
    profile = Profile.objects.get(id=pk)
    context = {'type': 'edit', 'profile': profile}
    return render(request, 'otzovik_app/registration_page.html', context)


def login_page(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, f'User {username} does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Password is incorrect')
    return render(request, 'otzovik_app/login_page.html', context)


@login_required(login_url='login_page')
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url="login_page")
def edit_restaurant(request, pk):
    restaurant = Restaurant.objects.get(id=pk)

    if request.method == "POST":
        restaurant.name = request.POST.get("name")
        restaurant.description = request.POST.get("description")
        restaurant.address.city = request.POST.get("city")
        restaurant.address.street = request.POST.get("street")
        restaurant.address.building = request.POST.get("building")
        restaurant.addressforgoogle.lat = request.POST.get("lat")
        restaurant.addressforgoogle.lng = request.POST.get("lng")
        restaurant.address.save()
        restaurant.addressforgoogle.save()
        restaurant.save()
        return redirect("restaurant_main", restaurant.id)

    cuisines = RestaurantCuisine.objects.all()
    context = {"restaurant": restaurant, "cuisines": cuisines, "type": "edit"}
    return render(request, "otzovik_app/new_restaurant.html", context)


@login_required(login_url='login_page')
def new_restaurant(request):
    if request.method == "POST":
        restaurant = Restaurant.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            short_description=request.POST.get('short_description'),
            profile=request.user.profile,
        )
        Address.objects.create(
            restaurant=restaurant,
            city=request.POST.get('city'),
            street=request.POST.get('street'),
            building=request.POST.get('building'),
        )
        AddressForGoogle.objects.create(
            restaurant=restaurant,
            lat=request.POST.get('lat'),
            lng=request.POST.get('lng'),
        )
        ReviewSummary.objects.create(
            restaurant=restaurant
        )

        cuisines = request.POST.getlist("cuisines")[:3]
        print(cuisines)
        for cuisine in cuisines:
            restaurant.cuisines.add(RestaurantCuisine.objects.get(id=cuisine))

        form = PreviewImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_form = form.save(commit=False)
            image_form.restaurant = restaurant
            image_form.save()

        images = request.FILES.getlist("images")
        for image in images:
            created_image = RestaurantImage.objects.create(image=image, restaurant=restaurant)
            created_image.save()

        return redirect('home')
    cuisines = RestaurantCuisine.objects.all()
    cuisines_list = [cuisine.cuisine for cuisine in cuisines]
    context = {
        "cuisines": cuisines,
        "cuisines_list": cuisines_list,
        # "restaurant_form": RestaurantForm(),
        # "address_form": AddressForm(),
        # "address_for_google_form": AddressForGoogleForm(),
        # "preview_image_form": PreviewImageForm(),
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
        validate_password(request.GET.get("password"))
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
