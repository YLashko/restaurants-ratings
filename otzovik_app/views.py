from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *


def home_page(request):
    content = '' if request.GET.get('search_for') is None else request.GET.get('search_for')
    context = {"content": content}
    return render(request, 'otzovik_app/home.html', context)


def registration_page(request):
    context = {}
    if request.method == 'POST':
        user = User.objects.create(
            username=request.POST.get('login'),
            password=request.POST.get('password'),
        )
        Profile.objects.create(
            name=request.POST.get('name'),
            surname=request.POST.get('surname'),
            email=request.POST.get('email'),
            user=user,
        )
        login(request, user)
        return redirect('home')
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


def logout_user(request):
    logout(request)
    return redirect('home')


def new_restaurant(request):
    context = {}
    if request.method == "POST":
        restaurant = Restaurant.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
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
        return redirect('home')

    return render(request, 'otzovik_app/new_restaurant.html', context)
