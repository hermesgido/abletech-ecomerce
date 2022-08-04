from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("admins", views.admins, name="admins"),
    path("data", views.datafilter, name="data"),
    path("dashboard", views.dashboard, name="dashboard"),
    
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

