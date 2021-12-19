from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('email', 'avatar')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Enter email', required=False)
    avatar = forms.ImageField(label='avatar', required=False)

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password1', 'password2', 'avatar')
