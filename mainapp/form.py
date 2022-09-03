from django import forms
from . models import *



class MainForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserRegForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'full_name', 'phone')


class ShopForm(MainForm):

    class Meta:
        model = Shops
        fields = '__all__'
        exclude = ['id', 'user_id']

    ''' def __init__(self, *args, **kwargs):
        super(ShopForm, self).__init__(*args, **kwargs)
        self.fields['sub_category'].queryset = Sub_Categories.objects.none

        if 'category' in self.data:
            try:
                shop_category_id = int(self.data.get('shop_category_id'))
                self.fields['sub_category'].queryset = Sub_Categories.objects.filter(
                    shop_category_id=shop_category_id)
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['sub_categories'].queryset = self.instance.shop_category_id.sub_category
 '''

class ProductForm(MainForm):
    class Meta:
        model = Product
        exclude = ['id','shop_id']
class PictureForm(MainForm):
    class Meta:
        model = Picture
        exclude = ['id', 'product_id']
        
class Product_AttributeForm(MainForm):
    class Meta:
        model = Product_Attribute
        exclude = ['id','product_id']
