from calendar import monthrange
from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from django.shortcuts import render, redirect

from .forms import LoginForm, SingUpForm, ExpenseForm, RevenueForm, BudgetForm
from .models import Budget, Category, Expense, Revenue


@login_required(login_url='/login')
def budget(request: WSGIRequest):
    user = request.user
    budgets = Budget.objects.filter(user=user)

    if request.method == 'POST':
        form = BudgetForm(request.POST)

        if form.is_valid():
            for b in budgets:
                match b.category.category:
                    case 'F':
                        b.percentage = form.cleaned_data['fixed']
                    case 'G':
                        b.percentage = form.cleaned_data['goal']
                    case 'I':
                        b.percentage = form.cleaned_data['investment']
                    case 'K':
                        b.percentage = form.cleaned_data['knowledge']
                    case 'P':
                        b.percentage = form.cleaned_data['pleasures']

                b.save()

            return redirect('index')
    else:
        data = {b.category.get_category_display().lower(): b.percentage for b in budgets}
        form = BudgetForm(initial=data)

    return render(
        request,
        'main/budget.html',
        context={
            'form': form
        }
    )


@login_required(login_url='/login')
def expense(request: WSGIRequest):
    user = request.user

    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            form.save(user)
            return redirect('index')
    else:
        form = ExpenseForm()

    return render(
        request,
        'main/expense.html',
        context={
            'form': form
        }
    )


@login_required(login_url='/login')
def revenue(request: WSGIRequest):
    user = request.user

    if request.method == 'POST':
        form = RevenueForm(request.POST)

        if form.is_valid():
            form.save(user)
            return redirect('index')
    else:
        form = RevenueForm()

    return render(
        request,
        'main/revenue.html',
        context={
            'form': form
        }
    )


@login_required(login_url='/login')
def index(request: WSGIRequest):
    user = request.user
    budgets = Budget.objects.filter(user=user)
    initial_date = date.today().replace(day=1)
    day = monthrange(initial_date.year, initial_date.month)[1]
    final_date = initial_date.replace(day=day)

    if len(budgets) == 0:
        categories = Category.objects.all()

        for category in categories:
            Budget.objects.create(category=category, user=user)

        budgets = Budget.objects.filter(user=user)

    expenses = Expense.objects.filter(user=user, date__range=(initial_date, final_date))
    expenses_by_category = (Expense.objects
                            .filter(user=user, date__range=(initial_date, final_date))
                            .values('category')
                            .annotate(sum=Sum('value')))

    for e in expenses_by_category:
        e['category'] = (e['category'].replace('F', 'Fixed')
                         .replace('G', 'Goal')
                         .replace('I', 'Investment')
                         .replace('K', 'Knowledge')
                         .replace('P', 'Pleasures'))

    total_spent = sum(e.value for e in expenses)
    revenues = Revenue.objects.filter(user=user, date__range=(initial_date, final_date))
    total_earned = sum(r.value for r in revenues)
    return render(
        request,
        'main/index.html',
        context={
            'budgets': budgets,
            'expenses': expenses,
            'revenues': revenues,
            'expenses_by_category': expenses_by_category,
            'total_spent': total_spent,
            'total_earned': total_earned
        }
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
