from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .config import EMAIL_REGEX_PATTERN
import re
from django.contrib.auth.password_validation import validate_password, ValidationError
from django.utils.translation import gettext as _

from .validations import validate_email, validate_username, validate_restaurant_name


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
        fields = ['city', 'street', 'building']


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
