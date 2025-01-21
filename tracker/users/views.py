from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import UserLoginForm, UserCreateForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib import messages

# Create your views here.


def login_user(request):

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('tracker:home'))
            # elif form.cleaned_data['username'] is None:
            if not get_user_model().objects.filter(username=cd['username']).exists():
                return HttpResponseRedirect(reverse('users:registration'))
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('tracker:home'))


class RegisterUser(CreateView):
    form_class = UserCreateForm
    template_name = 'users/registration.html'
    extra_context = {'title': "Registration"}
    success_url = reverse_lazy('users:login')


