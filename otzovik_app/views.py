from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import PreviewImageForm
from .models import *


def home_page(request):
    content = '' if request.GET.get('search_for') is None else request.GET.get('search_for')
    restaurants = Restaurant.objects.all()
    context = {'content': content, 'restaurants': restaurants}
    return render(request, 'otzovik_app/home.html', context)


def registration_page(request):
    context = {'type': 'register'}
    if request.method == 'POST':
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
            messages.error(request, f'Password is incorrect')
    return render(request, 'otzovik_app/login_page.html', context)


@login_required(login_url='login_page')
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login_page')
def new_restaurant(request):
    context = {}
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
        form = PreviewImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_form = form.save(commit=False)
            image_form.restaurant = restaurant
            image_form.save()
        return redirect('home')

    return render(request, 'otzovik_app/new_restaurant.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile}
    if request.method == 'POST':
        profile.unp = request.POST.get('unp')
        profile.save()
        return redirect('user_profile', profile.id)
    return render(request, 'otzovik_app/user_profile.html', context)


def restaurant_main(request, pk):
    restaurant = Restaurant.objects.get(id=pk)
    reviews = Review.objects.filter(restaurant=restaurant).all()
    context = {'restaurant': restaurant, 'reviews': reviews}
    return render(request, 'otzovik_app/restaurant_main.html', context)


@login_required(login_url='login_page')
def new_review(request, pk):
    restaurant = Restaurant.objects.get(id=pk)
    try:
        Review.objects.get(profile_id=request.user.id, restaurant=restaurant)
        messages.error(request, 'Вы уже написали отзыв на этот рестоан!')
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
        return redirect('restaurant_main', restaurant.id)

    context = {'restaurant': restaurant}
    return render(request, 'otzovik_app/new_review.html', context)
