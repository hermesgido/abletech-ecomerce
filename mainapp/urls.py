from django.urls import path
from . import views
from . import adminviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    #path("", HomePageListView.as_view(), name="HomePageListView"),
    
    
    
    
    path('wellcome', views.wellcome, name="wellcome"),
    path("", views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),    
    path("logout_user", views.logout_user, name="logout_user"),
    path('product_details/<str:id>/', views.product_details, name="product_details"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("my_account", views.my_account, name="my_account"),
    path("my_orders", views.my_orders, name="my_orders"),
    path("chart", views.chart, name="chart"),
    path("privacy_policy", views.privacy_policy, name="privacy_policy"),
    path("support", views.support, name="support"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("shops_list", views.shops_list, name="shops_list"),
    path('category/<str:id>/', views.category, name="category"),
    path("sub_category/<str:id>/", views.sub_category, name="sub_category"),
    path("shops_products", views.shop_products, name="shop_products"),
    path("checkout_payment", views.checkout_payment, name="checkout_payment"),
    path("bank_payment", views.bank_payment, name="bank_payment"),
    path("cash_payment", views.cash_payment, name="cash_payment"),
    path("payment_success", views.payment_success, name="payment_success"),
    path("product/<str:id>", views.product, name="product"),
    

    path('accounts/password_reset/', views.password_change, {"template_name":"templates/registration/change_password.html"}, name='password_reset'),
  
  
   path("update_item/", views.update_item, name = "update_item"),
    
    #####SELLER DASHBOARD URLS
    path("dashboard", views.dashboard, name="dashboard"),
    path("all_products", views.all_products, name="all_products"),
    path("shop_setting", views.shop_setting, name="shop_setting"),
    path("edit_product/<str:id>/", views.edit_product, name="edit_product"),

    path('load_sub_categories', views.load_sub_categories, name="load_sub_categories"),
    path("add_product", views.add_product, name="add_product"),
    path('added_products', adminviews.added_products, name="added_products"),
    path("upload_pictures/<str:id>/", views.upload_pictures, name="upload_pictures"),
    path("orders", views.orders, name="orders"),
    
    #####ADMIN dASHBOARD URLS#######
    path("admins", views.admins, name="admins"),
    path("register_seller", views.register_seller, name="register_seller"),
    path("sellers_list", views.sellers_list, name="sellers_list"),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


