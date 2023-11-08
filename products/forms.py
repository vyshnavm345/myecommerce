from django.contrib.auth.forms import UserCreationForm
from .models import Custom_User, Product, Pc, Monitor, Keyboard, Category, SubCategory, Headphone, Address, Return, Offers
from django import forms
class CreateUserForm(UserCreationForm):
    status = forms.ChoiceField(
        choices=Custom_User.STATUS_CHOICES,
        initial='Active',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Custom_User
        fields = ['username', 'email', 'password1', 'password2', 'status', 'image', 'phone']
  
  
  
  
######################################################Products##################################################################### 

# Products   

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  

class PcForm(ProductForm):
    class Meta:
        model = Pc
        exclude = ['product_ptr']  

class MonitorForm(ProductForm):
    class Meta:
        model = Monitor
        exclude = ['product_ptr']  

class KeyboardForm(ProductForm):
    class Meta:
        model = Keyboard
        exclude = ['product_ptr']

class HeadphoneForm(ProductForm):
    class Meta:
        model = Headphone
        exclude = ['product_ptr']



#######################################################Categories#################################################################

# Categories

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__' 
        
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__' 
        
        
###################################################### Address Form ################################################################

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        
        
###################################################### RETURNS #####################################################################

# returns
class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['reason']
        
class MainOfferForm(forms.ModelForm):
    class Meta:
        model = Offers
        fields = '__all__' 
        widgets = {
            "description": forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 25rem;'}),
        }