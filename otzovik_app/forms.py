from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .config import EMAIL_REGEX
from django.contrib.auth.password_validation import validate_password, ValidationError
from django.utils.translation import gettext as _


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'short_description', 'cuisines']


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'street', 'building']


class AddressForGoogleForm(ModelForm):
    class Meta:
        model = AddressForGoogle
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
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    class Meta:
        model = Profile
        fields = ['name', 'surname', 'email']

    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     if len(name) < 3:
    #         raise ValidationError(_('Username is too short'))

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if not EMAIL_REGEX.match(email):
    #         raise ValidationError(_('Invalid email'))


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username"]

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
