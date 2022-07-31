from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("admins", views.admins, name="admins"),
    path("dashboard", views.dashboard, name="dashboard"),
]
