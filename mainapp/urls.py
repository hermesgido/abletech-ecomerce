from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout_user", views.logout_user, name="logout_user"),

    
    
    #####SELLER DASHBOARD URLS
    path("dashboard", views.dashboard, name="dashboard"),
    path("add_shop", views.add_shop, name="add_shop"),
    path("shop_setting", views.shop_setting, name="shop_setting"),
    path("product_details", views.product_details, name="product_details"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("my_account", views.my_account, name="my_account"),
    path("about", views.about, name="about"),

    path('load_sub_categories', views.load_sub_categories, name="load_sub_categories"),
    path("add_product", views.add_product, name="add_product"),
    path('added_products', views.added_products, name="added_products"),
    path("upload_pictures/<str:id>/", views.upload_pictures, name="upload_pictures"),
    
    #####ADMIN dASHBOARD URLS#######
    path("admins", views.admins, name="admins"),
    path("register_seller", views.register_seller, name="register_seller"),
    path("sellers_list", views.sellers_list, name="sellers_list"),
    
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)


