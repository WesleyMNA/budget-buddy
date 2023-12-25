from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from .forms import LoginForm, SingUpForm


@login_required(login_url='/login')
def index(request: WSGIRequest):
    return render(
        request,
        'main/index.html'
    )


def login_view(request: WSGIRequest):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.errors['__all__'] = form.error_class(['username or password invalid'])
    else:
        form = LoginForm()

    return render(
        request,
        'main/login.html',
        context={
            'form': form
        }
    )


def logout_view(request: WSGIRequest):
    logout(request)
    return redirect('login')


def sing_up(request: WSGIRequest):
    if request.method == 'POST':
        form = SingUpForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = make_password(form.cleaned_data['password'])
            User.objects.create(
                first_name=name,
                username=username,
                email=email,
                password=password
            )
            return redirect('login')
    else:
        form = SingUpForm()

    return render(
        request,
        'main/sing-up.html',
        context={
            'form': form
        }
    )
