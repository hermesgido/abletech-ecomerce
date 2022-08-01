from django.contrib import admin

# Register your models here.
from .models import User
from .models import seller,Shop_Categories,Shops,Sub_shop_Categories,Cart,Product,Product_Picture,Product_Attribute,Order,Delivery_Details
from .models import Buyer, Delivery_Person
admin.site.register(User)

#########################################################################################
#######################Seller Registration##############################################
admin.site.register(seller)
admin.site.register(Shop_Categories)
admin.site.register(Shops)
admin.site.register(Sub_shop_Categories)
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(Product_Picture)
admin.site.register(Product_Attribute)
admin.site.register(Order)
admin.site.register(Delivery_Details)
##########################################################################################
######################Buyer Registration##################################################
admin.site.register(Buyer)
admin.site.register(Delivery_Person)

#########################################################################################