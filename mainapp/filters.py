from pyexpat import model
from .models import *
import django_filters
from django_filters import DateFromToRangeFilter
from django_filters import RangeFilter
from django_filters import BooleanFilter



class ProductFilter(django_filters.FilterSet):
    date_range  = DateFromToRangeFilter(field_name='posted_Date', lookup_expr='gte', label="Posted From")    
    price_from_to = RangeFilter(field_name='price', label= ' Price Range')
    class Meta:
        model= Product
        fields  = '__all__'
        exclude = ['shop_id','description', 'manufactured_Date', 'product_name']