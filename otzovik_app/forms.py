from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .config import EMAIL_REGEX_PATTERN
import re
from django.contrib.auth.password_validation import validate_password, ValidationError
from django.utils.translation import gettext as _

from .validations import validate_email, validate_username, validate_restaurant_name, validate_review_score, \
    validate_phone_number, validate_nip


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'short_description', 'cuisines']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        validate_restaurant_name(name)
        return name


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'building']


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']


class CoordinatesForm(ModelForm):
    class Meta:
        model = Coordinates
        fields = ['lat', 'lng']


class PreviewImageForm(ModelForm):
    class Meta:
        model = PreviewImage
        fields = ['preview_image']


class CuisineForm(ModelForm):
    class Meta:
        model = RestaurantCuisine
        fields = ['cuisine']


class ProfileForm(ModelForm):
    name = forms.CharField(max_length=200)
    surname = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)

    class Meta:
        model = Profile
        fields = ['name', 'surname', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        return email


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username"]

    def clean_password(self):
        password = self.cleaned_data.get('password1')
        validate_password(password)
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_username(username)
        return username


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['food_quality', 'staff_quality', 'price', 'body']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        validate_review_score(price)
        return price

    def clean_food_quality(self):
        food_quality = self.cleaned_data.get('food_quality')
        validate_review_score(food_quality)
        return food_quality

    def clean_staff_quality(self):
        staff_quality = self.cleaned_data.get('staff_quality')
        validate_review_score(staff_quality)
        return staff_quality


class CompanyProfileForm(ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'phone_number', 'nip', 'owner_name', 'owner_surname', 'description']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        validate_phone_number(phone_number)
        return phone_number

    def clean_nip(self):
        nip = self.cleaned_data.get('nip')
        validate_nip(nip)
        return nip
