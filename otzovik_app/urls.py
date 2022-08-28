from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('new_restaurant/', new_restaurant, name='new_restaurant'),
    path('register/', registration_page, name='registration'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_user, name='logout'),
    path('user/<str:pk>', user_profile, name='user_profile'),
    path('edit/<str:pk>', edit_profile, name='edit_profile'),
    path('restaurant/<str:pk>', restaurant_main, name='restaurant_main'),
    path('new_review/<str:pk>', new_review, name='new_review')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
