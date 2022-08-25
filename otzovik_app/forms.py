from django.forms import ModelForm
from .models import *


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'short_description']


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
