from django.shortcuts import redirect, render
from django.db.models import Count
from .form import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    top_shops = Shops.objects.all().order_by('shop_name')[:5]
    user_shop = Shops.objects.filter(seller_id__user_id__id=request.user.id)
    print(user_shop.query)

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

        if password != password1:
            messages.error(request, "Password dont Match")
            return redirect(signup)
        if len(password) < 4:
            messages.error(request, "Password too short")
            return redirect(signup)
        if User.objects.filter(username=username):
            messages.error(request, "user name already exist!")
            return redirect(signup)
        if User.objects.filter(email=email):
            messages.error(request, "email  already exist!")
            return redirect(signup)
        else:
            myUser = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                type_Of_User="B",
            )
            buyer = Buyer.objects.create(user_id=myUser)
            myUser.save()
            buyer.save()
            messages.success(request, "successfull registered")
            return redirect(signin)

    return render(request, "register.html")


def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "logged in...")
            return redirect(home)
        else:
            messages.error(request, "wrong details")
            return redirect(signin)

    return render(request, "login.html")


def product_details(request):
    
    return render(request, "front/product-details.html")
def cart(request):
    
    return render(request, "front/cart.html")
def checkout(request):
    
    return render(request, "front/checkout.html")
def about(request):
    
    return render(request, "front/about.html")


def my_account(request):
    return render(request, "front/my-account.html")

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
    shopform = ShopForm(request.POST, instance=seller_shop)

    if request.method == "POST":
        seller_shop = Shops.objects.get(seller_id__user_id__id=request.user.id)
        shopform = ShopForm(request.POST, instance=seller_shop)

    context = {'shopform': shopform}
    return render(request, "dashboard/shop_setting.html", context)


@login_required
def dashboard(request):
    if request.user.type_Of_User == "B":
        return redirect(home)

    seller_shop = Shops.objects.get(seller_id__user_id__id=request.user.id)
    print(seller_shop.shop_name)
    return render(request, "dashboard/dashboard.html", {'seller_shop': seller_shop})


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

    if request.method == "POST":
        productForm = ProductForm(request.POST)
        if productForm.is_valid():
            product_name = productForm.cleaned_data['product_name']
            price = productForm.cleaned_data['price']
            description = productForm.cleaned_data['description']
            brand_name = productForm.cleaned_data['brand_name']
            manufactured_Date = productForm.cleaned_data['manufactured_Date']
            shop_id = shop_id

            product = Product.objects.create(
                product_name=product_name, brand_name=brand_name, price=price,
                description=description, manufactured_Date=manufactured_Date, shop_id=shop_id
            )
            product.save()
            return redirect(added_products)

    context = {'productForm': productForm, 'pictureForm': pictureForm,
               'attributeForm': attributeForm}
    return render(request, "dashboard/add_product.html", context)


def added_products(request):

    # select all products of a current seller
    # and count pictures of each product(annotate)
    # and count attributes of each product(annotate)(distinct=true to aoid duplicates)
    products = Product.objects.filter(
        shop_id__seller_id__user_id=request.user.id).annotate(
            ptp=Count('product_picture', distinct=True)).order_by(
                '-posted_Date').annotate(
                attrs=Count('product_attribute', distinct=True))
    print(products.query)
    
    

    context = {'products': products,}

    return render(request, "dashboard/added_products.html", context)


def upload_pictures(request, id):
    product_id = Product.objects.get(id=id)
    pictureForm = PictureForm()
    if request.method == "POST":
        pictureForm = PictureForm(request.POST, request.FILES)
        if pictureForm.is_valid():
            product_picture = pictureForm.cleaned_data['product_picture']
            product_id = product_id
            pictures = Product_Picture.objects.create(
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
