from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from .forms import LoginForm, SingUpForm


@login_required(login_url='/login')
def index(request: WSGIRequest):
    return render(
        request,
        'main/index.html'
    )


def login(request: WSGIRequest):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            return
    else:
        form = LoginForm()

    return render(
        request,
        'main/login.html',
        context={
            'form': form
        }
    )


def sing_up(request: WSGIRequest):
    if request.method == 'POST':
        form = SingUpForm(request.POST)

        if form.is_valid():
            return
    else:
        form = SingUpForm()

    return render(
        request,
        'main/sing-up.html',
        context={
            'form': form
        }
    )
