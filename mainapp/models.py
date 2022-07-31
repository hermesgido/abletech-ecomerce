from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

######################################################################################
####################users models#####################################################


class User(AbstractUser):
    phone = models.CharField(max_length=12, blank=True)
    user_Lists = (("S", "Seller"), ("B", "Buyer"), ("D", "Delivery Person"))
    type_Of_User = models.CharField(
        max_length=10, choices=user_Lists, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

########################################################################################
######################sellers models####################################################


class seller(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, auto_created=True, verbose_name="USER ID")
    seller_id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="SELLER ID")
    Contact = models.CharField(max_length=12)
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    address = models.CharField(max_length=10)

    class Meta:
        db_table = 'sellers'
        verbose_name = "SELLER"
        verbose_name_plural = "SELLERS"
    
    def __str__(self):
        pass


class Shop_Categories(models.Model):
    seller_id = models.ForeignKey(
        seller, on_delete=models.CASCADE, auto_created=True, verbose_name="SELLER ID")
    category_id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="CATEGORY ID")
    category_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'categories'
        verbose_name = "SHOP CATEGORY"
        verbose_name_plural = "SHOP CATEGORIES"
    def __str__(self):
        return self.category_name


class Shops(models.Model):
    shop_category_id = models.ForeignKey(
        Shop_Categories, on_delete=models.CASCADE, auto_created=True, verbose_name="SHOP CATEGORY ID")
    shop_id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="SHOP ID")
    shop_name = models.CharField(max_length=12)
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    address = models.CharField(max_length=10)
    Contact = models.CharField(max_length=12)
    registered_Date = models.DateField()
    logo = models.ImageField(upload_to='seller logo/', blank=True)

    class Meta:
        db_table = 'shops'
        verbose_name = "SHOP"
        verbose_name_plural = "SHOPS"
    
    def __str__(self):
        return self.shop_name


class Sub_shop_Categories(models.Model):
    shop_category_id = models.ForeignKey(
        Shop_Categories, on_delete=models.CASCADE, auto_created=True, verbose_name="SHOP CATEGORY ID")
    sub_category_id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="SUB CATEGORY ID")
    sub_category_name = models.CharField(max_length=200)
    picture = models.ImageField(
        upload_to='ShopSubCategoryPicture/', blank=True)

    class Meta:
        db_table = 'sub_categories'
        verbose_name = "SUB SHOP CATEGORY"
        verbose_name_plural = "SUB SHOP CATEGORIES"
        
    def __str__(self):
            return self.sub_category_name


class Cart(models.Model):
    cart_id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="CART ID")
    product_id = models.CharField(max_length=200)
    unit_Price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()

    @property
    def Total(self):
        total_Price = self.Unit_Price * self.quantity
        return total_Price

    class Meta:
        db_table = 'carts'
        verbose_name = "CART"
        verbose_name_plural = "CARTS"
        
    def __str__(self):
        pass


class Product(models.Model):
    sub_category_id = models.ForeignKey(
        Sub_shop_Categories, on_delete=models.CASCADE, auto_created=True, verbose_name="SUB CATEGORY ID")
    cart_id = models.ForeignKey(
        Cart, on_delete=models.CASCADE, auto_created=True, verbose_name="CART ID")
    product_id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="PRODUCT ID")
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    posted_Date = models.DateTimeField()
    description = models.TextField()
    manufactured_Date = models.DateField()
    brand_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'products'
        verbose_name = "PRODUCT"
        verbose_name_plural = "PRODUCTS"
    
    def __str__(self):
        return self.product_name


class Product_Picture(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, auto_created=True, verbose_name="PRODUCT ID")
    picture_id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="PICTURE ID")
    picture_name = models.CharField(max_length=200)
    product_picture = models.ImageField(
        upload_to='ProductPicture/', blank=True)

    class Meta:
        db_table = 'product_pictures'
        verbose_name = "PRODUCT PICTURE"
        verbose_name_plural = "PRODUCT PICTURES"


class Product_Attribute(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, auto_created=True, verbose_name="PRODUCT ID")
    attribute_id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="ATTRIBUTE ID")
    attribute_name = models.CharField(max_length=200)
    value = models.TextField()

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
        User, on_delete=models.CASCADE, auto_created=True, verbose_name="USER ID")
    buyer_id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="BUYER ID")
    buyer_name = models.CharField(max_length=200)
    contact = models.CharField(max_length=12)
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    address = models.CharField(max_length=10)
    created_Date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'buyers'
        verbose_name = "BUYER"
        verbose_name_plural = "BUYERS"
        
        def __str__(self):
            return self.buyer_name
# 33


class Order(models.Model):
    buyer_order = models.ForeignKey(
        Buyer, on_delete=models.CASCADE, auto_created=True, verbose_name="BUYER ORDER ID")
    cart = models.OneToOneField(
        Cart, on_delete=models.CASCADE, auto_created=True, verbose_name="CART ID")
    order_id = models.AutoField(
        primary_key=True, auto_created=True, verbose_name="ORDER ID", unique=True)
    cutomer_id = models.CharField(max_length=200)
    created_Date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'
        verbose_name = "ORDER"
        verbose_name_plural = "ORDERS"
        
    def __str__(self):
        pass

class Delivery_Details(models.Model):
    order_id = models.OneToOneField(
        Order, on_delete=models.CASCADE, auto_created=True, verbose_name="ORDER ID")
    delivery_id = models.AutoField(
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
        User, on_delete=models.CASCADE, auto_created=True, verbose_name="USER ID")
    delivery_Person_id = models.AutoField(
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
            
    