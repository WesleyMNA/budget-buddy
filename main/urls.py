from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('budget', views.budget, name='budget'),
    path('expense', views.expense, name='expense'),
    path('revenue', views.revenue, name='revenue'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('singup', views.sing_up, name='singup'),
]
