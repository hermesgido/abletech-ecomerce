from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


####################users models#####################################################


class User(AbstractUser):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    user_Lists = (("S", "Seller"), ("B", "Buyer"), ("D", "Delivery Person"))
    type_Of_User = models.CharField(
        max_length=10, choices=user_Lists, blank=True)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(
        _("Profile Picture"), upload_to="profiles", default="profiles/profile-photo.jpg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'Users'
        verbose_name = "USER"
        verbose_name_plural = "USERS"

########################################################################################
######################sellers models####################################################


class Seller(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="USER ID")
    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="SELLER ID")
    Contact = models.CharField(max_length=12, null=True)
    longitude = models.CharField(max_length=200, null=True)
    latitude = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'sellers'
        verbose_name = "SELLER"
        verbose_name_plural = "SELLERS"


class Shop_Categories(models.Model):
    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="CATEGORY ID")
    category_name = models.CharField(max_length=200)
    picture = models.ImageField(
        _("Picture"), upload_to='Category Pics', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'categories'
        verbose_name = "SHOP CATEGORY"
        verbose_name_plural = "SHOP CATEGORIES"

    def __str__(self):
        return self.category_name


class Shops(models.Model):

    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="SHOP ID")
    shop_category_id = models.ForeignKey(
        Shop_Categories, on_delete=models.CASCADE, verbose_name="SHOP CATEGORY ID", null=True, blank=True)
    sub_category = models.ForeignKey(
        'Sub_Categories', on_delete=models.CASCADE, verbose_name="SUB CATEGORY ID", null=True, blank=True)
    seller_id = models.ForeignKey(
        Seller, on_delete=models.CASCADE, verbose_name="SHOP OWNER", null=True)

    shop_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    
    longitude = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=10, null=True, blank=True)
    Contact = models.CharField(max_length=12, null=True, blank=True)
    registered_Date = models.DateField(null=True, auto_now=True)
    logo = models.ImageField(upload_to='seller logo', blank=True, null=True)

    class Meta:
        db_table = 'shops'
        verbose_name = "SHOP"
        verbose_name_plural = "SHOPS"

    def __str__(self) -> str:
        return self.shop_name

class Sub_Categories(models.Model):
    shop_category_id = models.ForeignKey("Shop_Categories", null=True, verbose_name=_(
        "Sub Categories"), on_delete=models.CASCADE)
    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="SUB CATEGORY ID")
    sub_category_name = models.CharField(max_length=200)
    picture = models.ImageField(
        upload_to='ShopSubCategoryPicture', blank=True)

    class Meta:
        db_table = 'sub_categories'
        verbose_name = "SUB SHOP CATEGORY"
        verbose_name_plural = "SUB SHOP CATEGORIES"

    def __str__(self):
        return self.sub_category_name


class Product(models.Model):

    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="Product ID")
    shop_id = models.ForeignKey("Shops", verbose_name=_(
        "Shop ID"), on_delete=models.CASCADE, null=True)

    product_name = models.CharField(max_length=200)
    price = models.IntegerField(default=0, )
    posted_Date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    manufactured_Date = models.DateField()
    brand_name = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        db_table = 'products'
        verbose_name = "PRODUCT"
        verbose_name_plural = "PRODUCTS"

    def get_price(self):
        return ("{:,}".format(self.price))

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="Cart ID")
    product = models.ForeignKey("Product", verbose_name=_(
        "Product"), null=True, on_delete=models.CASCADE)
    order = models.ForeignKey("Order", verbose_name=_(
        "Order"), null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    @property
    def get_totals(self):
        total = self.product.price * self.quantity
        total_f = ("{:,}".format(total))
        return total_f



    class Meta:
        db_table = 'carts'
        verbose_name = "CART"
        verbose_name_plural = "CARTS"


class Picture(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="PRODUCT ID", related_name='pictures')
    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="PICTURE ID")
    picture_name = models.CharField(max_length=200, null=True, blank=True)
    product_picture = models.ImageField(
        upload_to='ProductPicture', blank=True)

    class Meta:
        db_table = 'product_pictures'
        verbose_name = "PRODUCT PICTURE"
        verbose_name_plural = "PRODUCT PICTURES"


class Product_Attribute(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="PRODUCT ID")
    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="ATTRIBUTE ID")
    attribute_name = models.CharField(max_length=200)
    value = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'product_attributes'
        verbose_name = "PRODUCT ATTRIBUTE"
        verbose_name_plural = "PRODUCT ATTRIBUTES"

    def __str__(self):
        return self.attribute_name
########################################################################################
#########################Buyers models###################################################


class Buyer(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="USER ID")
    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="BUYER ID")
    buyer_name = models.CharField(max_length=200, null=True, blank=True)
    contact = models.CharField(max_length=12, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    created_Date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'buyers'
        verbose_name = "BUYER"
        verbose_name_plural = "BUYERS"

        def __str__(self):
            return self.user_id.username + " " + "Order"



class Order(models.Model):
    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="Order ID", unique=True)
    buyer_id = models.ForeignKey(
        'Buyer', verbose_name='Buyer ID', null=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(
        'Shops', verbose_name='Shop ID', null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    @property
    def get_order_total(self):
        cart_total = self.cart_set.all()
        total_amount = sum([item.get_total for item in cart_total])
        return total_amount

    @property
    def get_cart_items(self):
        cart_items = self.cart_set.all()
        total = sum([self.item.quantity for item in cart_items])
        return total

    
    @property
    def get_cart_items(self):
        cart_items = self.cart_set.all()
        total = sum([self.item.quantity  for item in cart_items])
        totalf = ("{:,}".format(total))
        return  totalf






    class Meta:
        db_table = 'orders'
        verbose_name = "ORDER"
        verbose_name_plural = "ORDERS"

    def __str__(self):
        return self.buyer_id.user_id.username


class Delivery_Details(models.Model):
    order_id = models.OneToOneField(
        Order, on_delete=models.CASCADE, auto_created=True, verbose_name="ORDER ID")
    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="DERIVERY ID")
    shop_id = models.CharField(max_length=200)
    order_id = models.CharField(max_length=200)
    status = models.TextField()

    class Meta:
        db_table = 'delivery_details'
        verbose_name = "DELIVERY DETAIL"
        verbose_name_plural = "DELIVERY DETAILS"

    def __str__(self):
        return self.status

##########################################################################################
#########################Buyers models###################################################


class Delivery_Person(models.Model):
    person = models.OneToOneField(Delivery_Details, on_delete=models.CASCADE,
                                  auto_created=True, verbose_name="DELIVERY DETAIL ID")
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="USER ID")
    id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="DELIVERY PERSON ID")
    Contact = models.CharField(max_length=12)
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    address = models.CharField(max_length=10)
    email = models.EmailField()
    created_Date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'delivery_persons'
        verbose_name = "DELIVERY PERSON"
        verbose_name_plural = "DELIVERY PERSONS"

    def __str__(self):
        pass
