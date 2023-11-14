from django.contrib.auth.forms import UserCreationForm
from .models import Custom_User, Product, Pc, Monitor, Keyboard, Category, SubCategory, Headphone, Address, Return, Offers, Category_offer
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
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        
        for key, value in self.fields.items():
            value.widget.attrs.update({"class" : "form-control"})
            
        self.fields['is_variant'].widget.attrs.pop("class", None)
        # self.fields['rgb_support'].widget.attrs.pop("class", None)
        # self.fields['is_variant'].widget = forms.CheckboxInput()

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
    
    def __init__(self, *args, **kwargs):
        super(KeyboardForm, self).__init__(*args, **kwargs)
        
        # for key, value in self.fields.items():
        #     value.widget.attrs.update({"class" : "form-control"})
            
        self.fields['rgb_support'].widget.attrs.pop("class", None)
    
    


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


class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = Category_offer
        fields = '__all__'
        widgets = {
            "description": forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 25rem;'}),
            "category": forms.Select(attrs={'class': 'form-control'}),
        }