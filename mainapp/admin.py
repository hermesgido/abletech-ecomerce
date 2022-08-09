from django.contrib import admin

# Register your models here.
from .models import User
from .models import *
from .models import Buyer, Delivery_Person
admin.site.register(User)

#########################################################################################
#######################Seller Registration##############################################
admin.site.register(Seller)
admin.site.register(Shop_Categories)
admin.site.register(Shops)
admin.site.register(Sub_Categories)
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