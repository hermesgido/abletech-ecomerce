from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Count
from .form import *
from .models import *
from .adminviews import *
from mainapp import sellerviews
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, ListView
# Create your views here.



def added_products(request):
    
    # select all products of a current seller
    # and count pictures of each product(annotate)
    # and count attributes of each product(annotate)(distinct=true to aoid duplicates)
    products = Product.objects.filter(
        shop_id__seller_id__user_id=request.user.id).annotate(
            ptp=Count('pictures', distinct=True)).order_by(
                '-posted_Date').annotate(
                attrs=Count('product_attribute', distinct=True))
    print(products.query)

    context = {'products': products, }

    return render(request, "dashboard/added_products.html", context)