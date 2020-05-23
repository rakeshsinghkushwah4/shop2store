from django import forms
from django.contrib.auth.models import User
from seller.models import Product
from customer.models import OrderItem

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['slug','seller']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name'}),
            'price': forms.TextInput(attrs={'class':'form-control','placeholder':'Product Price'}),
            'category': forms.Select(attrs={"class":'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Product Description'}),
            }
class searchForm(forms.Form):
    Status = (('Status','Status'),('Panding','Panding'),('Delivered','Delivered'))
    try:
        product = Product.objects.all()
        pro = (('Product','Prodcut'),)
        for p in product:
            pro= pro+((str(p),str(p)),)
        status = forms.ChoiceField(choices=Status,required=False,initial='None')
        products = forms.ChoiceField(choices = pro,required=False,initial='None')
    except:
        pass

class orderForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['status']
