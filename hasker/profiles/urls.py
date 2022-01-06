from django.urls import path

from .views import MyProfileView
from .views import RegistrationView

app_name = 'profiles'

urlpatterns = [
    path('user/edit/', MyProfileView.as_view(), name='my-profile-view'),
    path('signup/', RegistrationView.as_view(), name='signup')
]
