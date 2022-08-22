from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('new_restaurant/', new_restaurant, name='new_restaurant'),
    path('register/', registration_page, name='registration'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_user, name='logout')
]