from django.urls import path
from .views import my_profile_view
from .views import registration_view

app_name = 'profiles'

urlpatterns = [
    path('user/edit/', my_profile_view, name='my-profile-view'),
    path('signup/', registration_view, name='signup')
]
