from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView

from .forms import ProfileModelForm, RegistrationForm
from .models import Profile


class MyProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileModelForm
    template_name = 'profiles/myprofile.html'
    extra_context = {'confirm': False}
    model = Profile
    
    def get_context_data(self, **kwargs):
        self.extra_context['profile'] = self.request.user
        return super(MyProfileView, self).get_context_data(**kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        self.extra_context['confirm'] = False
        return super(MyProfileView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        self.extra_context['confirm'] = True
        return render(self.request, 'profiles/myprofile.html', self.get_context_data())


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/signup.html'
    success_url = 'posts:main-post-view'

    def form_valid(self, form):
        user = form.save()
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        login(self.request, user)
        return redirect('posts:main-post-view')
