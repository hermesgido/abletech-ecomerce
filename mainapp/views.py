import json
from .filters import *
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Count, Q
from .form import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, ListView
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

# Create your views here.



def home(request):
    top_shops = Shops.objects.all().order_by('shop_name')[:5]
    user_shop = Shops.objects.filter(seller_id__user_id__id=request.user.id)
    

    return render(request, "index.html", {'top_shops': top_shops})


def signup(request):
    form = UserRegForm()
    myUser = User.objects.all()
    if request.method == "POST":
        form = UserRegForm(request.POST)
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password1 = request.POST["password1"]
        latitude=request.POST['latitude']
        longitude = request.POST['longitude']

        if password != password1:
            messages.error(request, "Password dont Match")
            return redirect(signup)
        if len(password) < 4:
            messages.error(request, "Password too short")
            return redirect(signup)
        if User.objects.filter(username=username).exists():
            messages.error(request, "user name already exist!")
            return redirect(signup)
        if User.objects.filter(email=email).exists():
            messages.error(request, "email  already exist!")
            return redirect(signup)
        else:
            myUser = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                type_Of_User="B",
            )
            buyer = Buyer.objects.create(user_id=myUser, latitude=latitude, longitude=longitude)
            myUser.save()
            buyer.save()
            messages.success(request, "successfull registered")
            return redirect(signin)

    return render(request, "costomer/register.html")


def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "logged in...")
            if request.user.type_Of_User == 'B':
                return redirect(home)
            if request.user.type_Of_User == 'S':
                return redirect(dashboard)
        else:
            messages.error(request, "wrong details")
            return redirect(signin)

    return render(request, "costomer/login.html")


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
    else:
       form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })

def wellcome(request):
    return render(request, "costomer/wellcome.html")


def home(request):
    top_5_products = Product.objects.all()[:5]
    featured_products = Product.objects.all().order_by('price')[:6]
    categories = Shop_Categories.objects.all()
    
    
    if  request.user.is_authenticated and request.user.type_Of_User == 'B':
    #count cart current items
        incomplete_order = Order.objects.filter(
                buyer_id__user_id = request.user.id, completed=False)
        for order in incomplete_order:
             cart_items = Cart.objects.filter(order=order).count()
    else:
        cart_items = 0    
    top_products = Product.objects.all().order_by('-posted_Date')
    
    
    
    #search funtionality in homepage
    if request.method == 'GET':
        query = request.GET.get('search')
        if query is not None:
            lookup = Q(Q(product_name__icontains = query) |
                       Q(description__icontains = query)|
                       Q(price__icontains = query))
            top_products = Product.objects.filter(lookup)
    else:
        top_products = Product.objects.all()
        
    
    context = {
        'top_products': top_products, 'top_5_products':top_5_products,
        'featured_products':featured_products,'cart_items':cart_items,
        'categories':categories
        }
    return render(request, 'costomer/home.html', context)
#class based view home view
''' class HomePageListView(TemplateView): # new
      model = Product
      context_object_name = 'top_products'
      template_name = 'costomer/home.html' '''
def product(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        quantity = request.POST['quantity']
    # add to cart
        buyer = Buyer.objects.get(user_id__id=request.user.id)
        orderqr = Order.objects.filter(buyer_id = buyer, completed=False)[:0]
  
        print("order dont exists")
        order, created = Order.objects.get_or_create(buyer_id=buyer, completed=False,)

        cart_item = Cart.objects.create(quantity=quantity, product=product, order=order)
        cart_item.save()
        
        
    product_shop = Shops.objects.get(product__id=product.id)

    shop_products = Product.objects.filter(shop_id__id=product_shop.id)
    print(shop_products)

    context = {'product': product, 'shop_products': shop_products}
        
    return render(request, "costomer/product.html", context)




def product_details(request, id):   
    product = Product.objects.get(id=id)
 
    shop = Shops.objects.get(product__id = product.id)
    if request.user.type_Of_User != "B":
        messages.error(request, "You must be a buyer to place order")
    else:
        if request.method == "POST":
            quantity = request.POST['quantity']
        # add to cart
            buyer = Buyer.objects.get(user_id__id=request.user.id)
            order, created = Order.objects.get_or_create(buyer_id=buyer, completed=False,shop=shop)
            order_qs = Order.objects.filter(buyer_id = buyer, completed=False, shop=shop)
            order = order_qs[0]
            if  Cart.objects.filter(order=order, product=product).exists():
                    cart_item = Cart.objects.get(order=order, product=product)
                    cart_item.quantity = quantity
                    cart_item.save()
            else:  
                cart_item = Cart.objects.create(quantity=quantity, product=product, order=order)
                cart_item.save()
            
       
    product_shop = Shops.objects.get(product__id=product.id)

    shop_products = Product.objects.filter(shop_id__id=product_shop.id)
    print(shop_products)

    context = {'product': product, 'shop_products': shop_products}
    return render(request, "costomer/single-product.html", context)


def cart(request):
    if  request.user.is_authenticated:
        buyer = Buyer.objects.get(user_id__id=request.user.id)
        orders = Order.objects.filter(buyer_id=buyer, completed=False)
        items=[]
        total_amount = 0
        for order in orders:
            total_amount = total_amount + order.get_order_total
            for i in order.cart_set.all():
                items.append(i)
        print(items)
        print(total_amount)
        get_order_total = ("{:,}".format(total_amount))
        
           
    else:
        items= []
    #delete an item in cart
    if request.method=="POST":
        itemId = request.POST['itemId']
        item = Cart.objects.get(id=itemId, order=order )
        item.delete()
        return redirect(cart)
    context={'items': items, 'get_order_total': get_order_total}
    return render(request, "costomer/cart.html", context)

def update_item(request):
    is_ajax = request.headers.get('X-Requested-Width') == 'XMLHttpRequest'
    data = json.loads(request.body)
    productId= data['productId']
    action= data['action']
    myuser = request.user
    buyer = Buyer.objects.get(user_id = myuser)
    product = Product.objects.get(id=productId)
    shop = Shops.objects.get(product__id = product.id)
    order, created = Order.objects.get_or_create(buyer_id=buyer, completed=False,shop=shop)
    cart_item , created = Cart.objects.get_or_create(product=product, order=order) 
    if action == 'add':
        cart_item.quantity = cart_item.quantity + 1
    elif action == 'remove':
        cart_item.quantity = cart_item.quantity-1
    cart_item.save()
    if cart_item.quantity<=0:
       cart_item.delete()
    
    cart_item = Cart.objects.get(product=product,order=order)
    cart_total = cart_total.quantity
        
    print(productId, data)
    return JsonResponse('Successfull...', safe=False)


@login_required
def checkout(request):
    
    if  request.user.is_authenticated:
        buyer = Buyer.objects.get(user_id__id=request.user.id)
        orders = Order.objects.filter(buyer_id=buyer, completed=False,)
        for order in orders:
            items = order.cart_set.all()
        
    else:
        items= []
    #delete an item in cart
    if request.method=="POST":
        itemId = request.POST['itemId']
        item = Cart.objects.get(id=itemId, order=order )
        item.delete()
        return redirect(cart)
    context={'items': items, 'order':order, 'buyer': buyer}
    return render(request, "costomer/checkout.html", context)





def my_account(request):
    return render(request, "costomer/settings.html")

def chart(request):
    return render(request, "costomer/message.html")

def my_orders(request):
    try:
       orders = Order.objects.filter(buyer_id__user_id = request.user.id)
       orders_total = Order.objects.filter(buyer_id__user_id = request.user.id).count()
       if orders_total <1:
           messages.info(request, "You dont have any order yet")
    except:
        messages.error = (request, "You haven't placed any order")
    
    context = {'orders': orders} 
    return render(request, "costomer/my-order.html", context)

def edit_profile(request):
    current_user = User.objects.get(id=request.user.id)
    print(current_user.username)
    if request.method == "POST":
        username = request.POST['username']
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        try:
           profile_pic = request.FILES['profile-pic']
        except:
            profile_pic = current_user.profile_pic
        if User.objects.filter(username=username).exists() and username != current_user.username:
           messages.error(request, "Username already exists")
           return redirect("edit_profile")
        if User.objects.filter(email=email).exists()and email != current_user.email:
           messages.error(request, "email already exists")
           return redirect("edit_profile")
        else:
            
            if profile_pic:
               current_user.profile_pic = profile_pic
               current_user.username = username
               current_user.save()
            else:
               current_user.username = username
               current_user.save() 
        return redirect(edit_profile)
            
    context = {'current_user': current_user}
    return render(request, "costomer/edit-profile.html", context)


def checkout_payment(request):
    return render(request, "costomer/checkout-payment.html")
def bank_payment(request):
    return render(request, "costomer/checkout-bank.html")
def cash_payment(request):
    return render(request, "costomer/checkout-cash.html")
def payment_success(request):
    return render(request, "costomer/payment-success.html")
    


def shops_list(request):
    
    return render(request, "costomer/vendors.html")

def shop_products(request):
    
    return render(request, "costomer/vendor-shop.html")


def support(request):
    return render(request, "costomer/support.html")
def privacy_policy(request):
    return render(request, "costomer/privacy-policy.html")


def category(request, id):
    category= Shop_Categories.objects.get(id=id)
    sub_categories = Sub_Categories.objects.filter(shop_category_id=category)
    
    context = {
        'category':category,'sub_categories':sub_categories,
    }
    return render(request, "costomer/category.html", context)

def sub_category(request, id):
    sub_category = Sub_Categories.objects.get(id=id)
    
    context = {
       'sub_category':sub_category 
    }
    return render(request, "costomer/sub-category.html", context)


def shops_details(request):
    return render(request, "costomer/vendor-shop.html")



########ADMIN DASHBOARD VIEWS########


def admins(request):
    return render(request, "admins/admins.html")


def register_seller(request):
    seller_shop = Shops.objects.filter(seller_id__user_id__id=request.user.id)
    print(seller_shop.query)
    form = UserRegForm()
    if request.method == "POST":
        form = UserRegForm(request.POST)
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        full_name = request.POST["full_name"]
        password = request.POST["password"]
        password1 = request.POST["password1"]

        if password != password1:
            messages.error(request, "Password dont Match")
            return redirect(register_seller)
        if len(password) < 4:
            messages.error(request, "Password too short")
            return redirect(register_seller)
        if User.objects.filter(username=username):
            messages.error(request, "user name already exist!")
            return redirect(register_seller)
        if User.objects.filter(email=email):
            messages.error(request, "email  already exist!")
            return redirect(register_seller)
        else:
            myUser = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                type_Of_User="S",
                phone=phone,
                full_name=full_name,
            )
            seller = Seller.objects.create(user_id=myUser)
            myUser.save()
            seller.save()
            seller_shop = Shops.objects.create(seller_id=seller)
            seller_shop.save()

            messages.success(request, "successfull registered")
            return redirect(admins)

    return render(request, "admins/register_seller.html")


def sellers_list(request):
    return render(request, "admins/sellers_list.html")


def logout_user(request):
    logout(request)
    return redirect(home)


#######seller dashboard views########
@login_required
def add_shop(request):
    if request.user.type_Of_User == "B":
        return redirect(home)
    shopform = ShopForm()
    seller_shop = Shops.objects.all()
    if request.method == "POST":
        shopform = ShopForm(request.POST)
        shop_name = request.POST['shop_name']
        longitude = request.POST['longitude']
        shop_category_id = request.POST['shop_category_id']
        latitude = request.POST['latitude']
        address = request.POST['address']
        Contact = request.POST['Contact']

        seller_id = Seller.objects.get(user_id=request.user.id)
        cat = Shop_Categories.objects.get(id=shop_category_id)
        seller_shop = Shops.objects.create(
            seller_id=seller_id,
            shop_name=shop_name, longitude=longitude, latitude=latitude,
            address=address, Contact=Contact, shop_category_id=cat
        )
        seller_shop.save()

    context = {'shopform': shopform, 'seller_shop': seller_shop}
    return render(request, "dashboard/add_shop.html", context)


def shop_setting(request):
    if request.user.type_Of_User == "B":
        return redirect(home)
    seller_shop = Shops.objects.get(seller_id__user_id__id=request.user.id)

    if request.method == "POST":
        seller_shop = Shops.objects.get(seller_id__user_id__id=request.user.id)
        Contact = request.POST['Contact']
        address = request.POST['address']   
        email = request.POST['email']     
        shop_name  = request.POST['shop_name']
        seller_shop.Contact = Contact
        seller_shop.address = address
        seller_shop.shop_name = shop_name
        seller_shop.email = email
        seller_shop.save()
        
    context = {'seller_shop': seller_shop}
    return render(request, "dashboard/shop_setting.html", context)

def all_products(request):
    product_filter = ProductFilter() 
    seller_shop = Shops.objects.get(seller_id__user_id__id=request.user.id)
    products = Product.objects.filter(shop_id = seller_shop).order_by('-posted_Date')

    productstt = Product.objects.filter(shop_id = seller_shop)
    total_products = productstt.count()
    
    if request.method == "POST" and 'delete' in request.POST:
        productID = request.POST['productID']
        product_to_delete = Product.objects.get(id=productID) 
        product_to_delete.delete()
        
        return redirect(all_products)
    product_filter = ProductFilter(request.GET, queryset = products ) 
    products  = product_filter.qs
        
    ''' is_ajax = request.headers.get('X-Requested-Width') == 'XMLHttpRequest'
    
    if is_ajax and request.method == "POST":
        data= json.loads(data)
        product_filter = ProductFilter(request.GET, queryset = products ) 
        products  = product_filter.qs.values()
        return  JsonResponse(products, safe=False) '''
        
    if products.count()<1:
        messages.info(request, "No Products found")
    context = {'products': products, 'total_products':total_products, 'product_filter': product_filter}
    return render(request, "dashboard/all-products.html", context)


def edit_product(request, id):
    product = Product.objects.get(id=id)
    product_filter = ProductFilter() 
    if request.method == "POST":
        manufactured_Date = request.POST['manufactured_Date']
        product_name = request.POST['product_name']
        price = request.POST['price']
        brand_name = request.POST['brand_name']
        description = request.POST['description']
        product.manufactured_Date = manufactured_Date
        product.price = price
        product.product_name = product_name
        product.description = description
        product.brand_name = brand_name
        product.save()
       
    context = {'product':product, 'product_filter': product_filter}
    return render(request, "dashboard/edit-product.html", context)

@login_required
def dashboard(request):
    if request.user.type_Of_User == "B":
        return redirect(home)
    seller_shop = Shops.objects.filter(seller_id__user_id__id=request.user.id)[0]
    total_products = Product.objects.filter(shop_id = seller_shop).count()
    total_orders = Order.objects.filter(shop=seller_shop).count()
    top_sold = Product.objects.filter(shop_id = seller_shop)
    total_sales=[]
    complited_orders = Order.objects.filter(shop=seller_shop, completed=True)
    for order in complited_orders:
        print(order.get_order_total)
        total_sales.append(order.get_order_total)
    
    total_sales= sum(total_sales)  
    total_sales= (("{:,}".format(total_sales)))
    
    
    #this month orders
    tis_month = Order.objects.filter(shop=seller_shop, completed=True)
    
    
    context = {'seller_shop': seller_shop, 'total_products': total_products, 
               'total_orders':total_orders, 'total_sales': total_sales, 'top_sold': top_sold}
    return render(request, "dashboard/dashboard.html", context)


def load_sub_categories(request):
    shop_category_id = request.GET.get('shop_category_id')
    sub_categories = Sub_Categories.objects.filter(
        shop_category_id=shop_category_id)
    return render(request, "dashboard/subcategories.html")


def add_product(request):
    productForm = ProductForm()
    pictureForm = PictureForm()
    attributeForm = Product_AttributeForm
    shop_id = Shops.objects.get(seller_id__user_id=request.user.id)
    pictureForm = PictureForm()
    if request.method == "POST":
        productForm = ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            product_name = productForm.cleaned_data['product_name']
            price = productForm.cleaned_data['price']
            description = productForm.cleaned_data['description']
            brand_name = productForm.cleaned_data['brand_name']
            manufactured_Date = productForm.cleaned_data['manufactured_Date']
            pictures = request.FILES.getlist('product_picture')
            shop_id = shop_id
            is_active = True

            product = Product.objects.create(
                product_name=product_name, brand_name=brand_name, price=price,
                description=description, manufactured_Date=manufactured_Date, shop_id=shop_id, is_active=is_active
            )
            product.save()

            for pic in pictures:
                product_pictures = Picture.objects.create(
                    product_picture=pic, product_id=product)
                product_pictures.save()
            return redirect(all_products)

    context = {'productForm': productForm, 'pictureForm': pictureForm,
               'attributeForm': attributeForm}
    return render(request, "dashboard/add_product.html", context)





def upload_pictures(request, id):
    product_id = Product.objects.get(id=id)
    pictureForm = PictureForm()
    if request.method == "POST":
        pictureForm = PictureForm(request.POST, request.FILES)
        if pictureForm.is_valid():
            product_picture = pictureForm.cleaned_data['product_picture']
            product_id = product_id
            pictures = Picture.objects.create(
                product_picture=product_picture, product_id=product_id)
            pictures.save()
            return redirect(added_products)

    context = {'product_id': product_id}
    return render(request, "dashboard/upload_picture.html", context)


def add_specs(request, id):

    product_id = Product.objects.get(id=id)
    attributeForm = Product_AttributeForm()
    if request.method == "POST":
        attributeForm = Product_AttributeForm(request.POST)
        if attributeForm.is_valid():
            attribute_name = attributeForm.cleaned_data['attribute_name']
            value = attributeForm.cleaned_data['value']
            product_id = product_id
            product_attribute = Product_Attribute.objects.create(
                attribute_name=attribute_name, product_id=product_id, value=value)
            product_attribute.save()
            return redirect(added_products)

    attrs = Product.objects.filter(
        shop_id__seller_id__user_id=request.user.id).order_by('-posted_Date').annotate(attrs=Count('product_attributes'))

    context = {'attrs': attrs, 'attributeForm': attributeForm}
    return render(request, "dashboard/add-specs.html", context)

def orders(request):
    
    user = request.user
    shop = Shops.objects.get(seller_id__user_id = user)
    orders = enumerate(Order.objects.filter(shop=shop).order_by('completed', 'created_date'), start =1)
    
    print(orders)
    context = {"orders": orders}
    return render(request, "dashboard/orders.html", context)