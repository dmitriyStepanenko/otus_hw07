from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProfileModelForm, RegistrationForm


@login_required
def my_profile_view(request):
    profile = request.user
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'profiles/myprofile.html', context)


def registration_view(request):

    form = RegistrationForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        user = form.save()

        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        login(request, user)
        return redirect('posts:main-post-view')

    context = {
        'form': form
    }

    return render(request, 'registration/signup.html', context)