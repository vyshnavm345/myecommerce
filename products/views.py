from django.shortcuts import render, redirect, get_object_or_404
from .models import Pc, Offers, Custom_User, Category, Product, SubCategory, ProductImages,Return, Wishlist, Cart, Address, Orders, OrderItems, Brand, Coupons, UserCoupons, Category_offer, Reviews
from .forms import CreateUserForm, PcForm, MonitorForm, KeyboardForm, CategoryForm, SubCategoryForm, HeadphoneForm, AddressForm, ReturnForm, MainOfferForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .utils import send_otp
from .func import get_product_form, variants, get_status, send_email_to_client
from datetime import datetime
import pyotp
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from .decorators import custom_login_required_with_message
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from wallet.models import Wallet, Transaction
from django.utils import timezone
from referals.models import ReferenceProfile
from decimal import Decimal
from django.http import FileResponse
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def home(request):
    products = Product.objects.all().order_by('product_name')
    subcategory = SubCategory.objects.get(name='Laptops')
    laptops = Pc.objects.filter(subcategories=subcategory)
 
    offer_list = Offers.objects.all()
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(brand__brand_name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    paginator = Paginator(products, 12) 

    # Get the current page number from the request's GET parameter
    page_number = request.GET.get('page')

    # Get the Page object for the current page number
    page = paginator.get_page(page_number)
    sale_items = Product.objects.filter(offer__is_active=True)[:9]
    
    context = {
        "products": page,
        "offers": offer_list,
        "laptops" : laptops,
        "sale_items" : sale_items,
    }
    return render(request, "shop_home_page.html", context)

@never_cache
def userLogin(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password = password)
      

        if user is not None:         
            request.session['username'] = username
            request.session['is_user'] = True
            request.session['otp_issued'] = False
            return redirect('otp')       
        else:
            messages.info(request, "Username or Password Incorrect")
    context = {}
    return render(request, "shop_login.html", context)

def userSignup(request):
    form = CreateUserForm
    
    if request.method == "POST":
        form_data = request.POST.copy()
        form_data['status'] = 'Active'
        
        form = CreateUserForm(form_data)
    
        if form.is_valid():
            # send otp...           
            request.session['temp_user_data'] = form_data
            request.session['is_user'] = False
            request.session['otp_issued'] = False
            
            return redirect('otp')
        else:
            messages.error(request, 'Error invalid credentials')
                   
    context = {"form": form}
    return render(request, "signup.html", context)

@never_cache
def otpview(request):
    if request.user.is_authenticated:
        return redirect("home")
    context = { }
    if 'otp_count' not in request.session:
        request.session['otp_count'] = 3
        
    if request.method == 'POST':
        otp = request.POST['otp'].strip()
        
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']
        
        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)
            
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    if request.session['is_user'] == True:
                        current_user = request.session['username']
                        user = Custom_User.objects.get(username=current_user)
                        if user.status == "Active":
                            login(request, user)
                        else:
                            
                            messages.error(request, '!!! You have been Blocked by the Admin !!!')
                            return redirect("userLogin")
                            
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                        del request.session['username']
                        del request.session['otp_count']
                        del request.session['otp_issued']
                        wishlist_product_id = request.session.get('wishlist_product_id')
                        if wishlist_product_id:
                            # Remove the product ID from the session
                            del request.session['wishlist_product_id']
                            # Redirect the user to the wishlist page with the product ID parameter
                            return redirect('add_to_wishlist', pk=wishlist_product_id)
                        return redirect('home')
                        
                    else:
                        user_data = request.session['temp_user_data']
                        form = CreateUserForm(data=user_data)  # Pass the user data to the form
                        if form.is_valid():
                            referal_id = request.session.get('ref_profile')
                            if referal_id is not None:
                                recommended_by_profile = ReferenceProfile.objects.get(id=referal_id)
                                instance = form.save()
                                registered_user = Custom_User.objects.get(id=instance.id)
                                registered_profile = ReferenceProfile.objects.get(user=registered_user)
                                registered_profile.recommended_by = recommended_by_profile.user
                                registered_profile.save()
                            else:
                                form.save()
                            user = form.cleaned_data.get('username')
                            messages.success(request,'Account was created for '+ user)
                            del request.session['otp_secret_key']
                            del request.session['otp_valid_date']
                            del request.session['temp_user_data']
                            del request.session['otp_count']
                            del request.session['otp_issued']
                            return redirect('userLogin')
                        else:
                        # Form is not valid, render the sign-up page with error messages
                            context['form'] = form
                            messages.error(request, 'Invalid form data. Please correct the errors.')
                            return render(request, 'signup.html', context)
                else:
                    messages.info(request,'invalid OTP')
                    request.session["otp_issued"] = True
                    return redirect("otp")
            else:
                messages.info(request,'OTP Expired')
        else:
            messages.info(request,'Something went wrong')
    if request.session['otp_issued'] == False:
        if request.session['otp_count'] > 0:
            send_otp(request)
        else:
            messages.info(request,'exceeded resend otp count')
                      
    return render(request, "shop_otp.html", context)

@never_cache
def resend_otp(request):
    request.session['otp_count']-=1
    request.session['otp_issued'] = False
    return redirect("otp")
   
def userLogout(request):
    request.session.clear()
    logout(request)
    return redirect('userLogin')
    
def adminSignin(request):
    context = {}
    return render(request, "adminLogin.html", context)

def product_detail(request, pk, clr=None):
    colors = []
    first = None
    try:
        product = Product.objects.get(pk=pk)
        
        products = Product.objects.all()[:4]
        offer_list = Offers.objects.all()
        var_list = variants(product)
        if clr == None:
            try:
                image_inst = ProductImages.objects.filter(product=product)
                for inst in image_inst:
                    if inst.color not in colors:
                        colors.append(inst.color)
                        
                if len(colors) > 0:
                    color = colors[0]
                    images = ProductImages.objects.filter(product=product, color=color)
                    first = ProductImages.objects.filter(product=product, color=color).first()

                else:
                    color = product.color
                    images = None
            except:
                color = product.color
        else:
            image_inst = ProductImages.objects.filter(product=product)
            for inst in image_inst:
                if inst.color not in colors:
                    colors.append(inst.color)
                        
            color = clr
            images = ProductImages.objects.filter(product=product, color=color)
            first = ProductImages.objects.filter(product=product, color=color).first()
            
        in_cart = False
        if request.user.is_authenticated:
            in_cart = Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
        
    except Product.DoesNotExist:
        return HttpResponseRedirect("Error Product does not exist")
    # first is the first instance of the productImage to diplay the main product picture in the product page
    # variants = get_variants(product)
    reviews = Reviews.objects.filter(product=product)
    context = {
        "product": product,
        "products":products,
        "offer_list": offer_list,
        "images" : images,
        "color" : color,
        "colors" : colors,
        "first" : first,
        "variants" : var_list,
        "in_cart" : in_cart,
        "reviews" : reviews,        
    }

    
    return render(request, "shop_product_details_page.html", context)

def demo(request):
    context={}
    return render(request, "shopedit.html",context)

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.info(request, "Invalid credentials.")
            return render(request, 'adminlogin.html', {})
    return render(request, 'adminlogin.html')

def admin_dashboard(request):
    customers = Custom_User.objects.all()
    if request.method == 'POST':
        request.POST.get()
    context = {
        "customers":customers,
    }
    return render(request, "dashboard.html", context)

def userstatus(request, pk):
    if request.method == "POST":
        user = Custom_User.objects.get(id=pk)
        
        if user.status == "Active":
            user.status = "Blocked"
        else:
            user.status = "Active"
        
        user.save()
    
    return redirect("admin_dashboard")

def adminLogout(request):
    logout(request)
    return redirect('adminlogin')

def adminCategoryManagement(request):
    form = CategoryForm
    search_query = request.GET.get('q', '')
    if request.method == "POST":
        category_name = request.POST['category_name']
        description = request.POST['description']
        
        existing_category = Category.objects.filter(Q(category_name__iexact=category_name)).first()
        
        if existing_category:
            messages.info(request, 'Category with this name already exists or is in the is_deleted list.')
            
            return redirect('admin_category')
        else:
            new_category = Category(category_name=category_name, description=description)
            new_category.save()
            messages.success(request, 'Category successfully created')
    
    if search_query:
        categories = Category.objects.filter(category_name__icontains=search_query, is_deleted=False)
    else:
        categories = Category.objects.filter(is_deleted=False)
    context = {
        "form": form,
        "categories": categories,
    }
    return render(request, "categoryManagement.html", context)

def view_deleted_categories(request):
    categories = Category.objects.filter(is_deleted=True)
    
    context = {
        "categories" : categories,
    }
    return render(request, "view_deleted_categories.html", context)

def view_deleted_subcategories(request):
    subcategories = SubCategory.objects.filter(is_deleted=True)
    
    context = {
        "subcategories" : subcategories,
    }
    return render(request, "view_deleted_subcategories.html", context)

def product_list(request):
    if request.method == 'POST':
        search_query = request.POST.get('q', '')  
        products = Product.objects.filter(product_name__icontains=search_query)
    else:
        products = Product.objects.all()    
    
    categories = Category.objects.all()
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')

    products_page = paginator.get_page(page_number)
    context = {
        "products": products_page,
        "categories": categories,
        "allproducts": products,
    }
    return render(request, 'product_list.html', context)


# go to the add product page and displays the list of product types to add
def add_product(request):
    # product_type = request.POST.get('data_value')
    # if product_type == 'pc':
    #     form_class = PcForm
    # elif product_type == 'monitor':
    #     form_class = MonitorForm
    # elif product_type == 'keyboard':
    #     form_class = KeyboardForm

    # if request.method == "POST":
    #     form = form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('product_list')
    # else:
    #     form = form_class()
    categories = Category.objects.all()
    context = {
        "categories" : categories
    }
    return render(request, 'addproduct.html', context)
# shows the prefilled product form to the user
def edit_product(request, pk):
    product_inst = Product.objects.get(id=pk)
    
    form_class = get_product_form(pk)
        
    if form_class is not None:   
        form = form_class(instance=product_inst)
    else:
        return redirect('product_list')
    
    context = {
        "form" : form
    }
    return render(request, "addProductForm.html", context)
    

  

def add_new_product(request, pk):
    if request.method == 'POST':
        action = request.POST['action']
        
        
        if action in ['Edit', 'Update']:
            product_inst = Product.objects.get(id=pk)
            category = product_inst.category
            product = category.category_name
            product_type = product.upper()
            product = f"assets/img/{ product}.jpg"
        
        elif action == 'Add':
            category = Category.objects.get(id=pk)
            product = category.category_name
            product_type = product.upper()
            product = f"assets/img/{ product}.jpg"
            
    else:
        category = Category.objects.get(id=pk)
        product = category.category_name
        product_type = product.upper()
        product = f"assets/img/{ product}.jpg"
    
    subcategories = category.subcategories.all()
    subcat = [i.name for i in subcategories]
           
    form_class = None
    
    categories = Category.objects.all()
    product_fields = [
        'product_name',
        'description',
        'price',
        'stock_quantity',
        'color',
        'brand', 
        'category',
        'subcategories',
        'image',
        'offer',
    ]
       
    if product_type == 'PC':
        form_class = PcForm
    elif product_type == 'MONITOR':
        form_class = MonitorForm
    elif product_type == 'KEYBOARD':
        form_class = KeyboardForm
    elif product_type == 'HEADPHONE':
        form_class = HeadphoneForm
        
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'Edit':
            
            form = form_class(instance=product_inst)
            
            form_instance = form_class()

            filtered_subcategories = form_instance.fields['subcategories'].queryset.filter(name__in=subcat)
            
           
            context = {
                "product_fields" : product_fields,
                "category" : category,
                "form": form,
                "subcategories": filtered_subcategories,
                "product" : product,
                "categories" : categories,
                "updating" : True,
                "product_inst" : pk,
                
            }
          
            return render(request, "addProductForm.html", context)
        
        if action == 'Update':
            
            product_id = request.POST.get('product_id')
            product_inst = Product.objects.get(id=pk)
            

            if 'image' in request.FILES:
                form = form_class(request.POST, request.FILES, instance=product_inst)
            else:
                form = form_class(request.POST, instance=product_inst)
            
            
            if form.is_valid():
                form.save()
                return redirect('product_list')
            else:
                print(form.errors)
                messages.info(request, "Invalid Data")
                return redirect('product_list')
            
            
        
        if action == 'Add':
            form = form_class(request.POST, request.FILES)
            form.instance.category = category
            if form.is_valid():
                form.save()
                messages.success(request, "Product Added Successfully")
            else:
                print(form.errors)
                messages.info(request, "Invalid Data")
                return redirect('add_product')
            
    
    
    if form_class is not None:
        # Create an instance of the form class
        form_instance = form_class()

        # Access the subcategories attribute on the form instance
        filtered_subcategories = form_instance.fields['subcategories'].queryset.filter(name__in=subcat)
    else:
        # Handle the case where form_class is None, e.g., by returning an error response
        return redirect('add_product')
    
    
    context = {
        "product_fields" : product_fields,
        "category" : category,
        "form": form_instance,
        "subcategories": filtered_subcategories,
        "product" : product,
        "categories" : categories,
        
    }   
    return render(request, "addProductForm.html", context)

def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    # product.delete()
    product.product_is_deleted = True
    product.save()
    return redirect('product_list')

def soft_deleted(request):
    soft_deleted_products = Product.all_objects.all()
    paginator = Paginator(soft_deleted_products, 5)

    page_number = request.GET.get('page')

    products_page = paginator.get_page(page_number)
    context = {
        "products": products_page,
    }
    return render(request, 'product_list.html', context)
    
def edit_category(request, pk):
    category = get_object_or_404(Category, id=pk)  # Retrieve the category or return a 404 if not found
    if request.method == 'POST':
        updating = False
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully')
            return redirect('admin_category')
    else:
        updating = True
        form = CategoryForm(instance=category)  # Initialize the form with the category data
    context = {
        "updating": updating,
        'form': form,
    }
    return render(request, 'categoryManagement.html', context)

def delete_category(request, pk):
    try:
        category = get_object_or_404(Category, id=pk)
        # category.delete()
        category.is_deleted = True
        category.save() 

        messages.success(request, 'category Removed')
    except:
        messages.error(request, 'category does not exist')
        
    return redirect('admin_category')

def restoreCategory(request, pk):
    try:
        category = get_object_or_404(Category, id=pk)
        category.is_deleted = False
        category.save() 
        messages.success(request, 'category Restored')
    except:
        messages.error(request, 'category does not exist')
        
    return redirect('admin_category')

def sub_category(request, pk):
    request.session["cat_id"] = pk
    subform = SubCategoryForm()
    category = Category.objects.get(pk=pk)
    subcategories = category.subcategories.filter(is_deleted = False)
    search_query = request.GET.get('q', '')
    
    if search_query:
        subcategories = SubCategory.objects.filter(category=category, name__icontains=search_query, is_deleted = False)
    else:
        subcategories = category.subcategories.filter(is_deleted = False)
    
    context = {

        "subcategories": subcategories,
        "subform": subform,  # Pass the subform to the template
        "updating": False,
        "id" : pk
    }
    return render(request, "categoryManagement.html", context)

def add_sub_category(request, pk=None):
    subcategories = {}
    # Get the subcategory or return a 404 if not found
    subcategory = get_object_or_404(SubCategory, id=pk) if pk else None
    subform = SubCategoryForm(instance=subcategory)
    if request.method == 'POST':
        sub_category_name = request.POST['name']
        description = request.POST['description']
        category = request.POST['category'] 
        category = Category.objects.get(id = category)
        action = request.POST['action']  # Get the action from the form
        if action == 'add':
            # Handle adding a new subcategory
            existing_category = SubCategory.objects.filter(Q(name__iexact=sub_category_name)).first()

            if existing_category:
                messages.info(request, 'Subcategory with this name already exists.')
            else:
                # Use the category_id from the subcategory to associate it with the correct category
                new_subcategory = SubCategory(name=sub_category_name, description=description, category=category)
                new_subcategory.save()
                messages.success(request, 'Subcategory successfully created')
        elif action == 'update':
            # Handle updating an existing subcategory
            subcategory.name = sub_category_name
            subcategory.description = description
            subcategory.category = category
            subcategory.save()
            messages.success(request, 'Subcategory Updated')
            cat_id = request.session["cat_id"]
            category = Category.objects.get(id=cat_id)
            subcategories = SubCategory.objects.filter(category=category)
            subform = SubCategoryForm()
            context = {
                "subcategories" : subcategories,
                "subform": subform,
                "id" : cat_id
            }
            return render(request, "categoryManagement.html", context)
    # If it's not a POST request (e.g., when initially rendering the form), set the default action to "add" and render the form
    
    context = {
        "subform": subform,
        "subcategory": subcategory,
        "action": "add" if pk is None else "update",  # Set the default action to "add"
    }
    return render(request, "categoryManagement.html", context)

def edit_sub_category(request, pk):
    subcategory = get_object_or_404(SubCategory, id=pk)
    
    subform = SubCategoryForm(instance=subcategory)        
    context = {
        "subform" : subform,
        "updating": True,
        "subcategory": subcategory,
    }
    return render(request, "categoryManagement.html", context)


def delete_sub_category(request, pk):
    try:
        subcategory = get_object_or_404(SubCategory, id=pk)
        # subcategory.delete()
        subcategory.is_deleted = True
        subcategory.save() 
        messages.success(request, 'Subcategory Removed')
    except:
        messages.error(request, 'Subcategory does not exist')
        
    return redirect('admin_category')

def restoreSubCategory(request, pk):
    try:
        subcategory = get_object_or_404(SubCategory, id=pk)
        subcategory.is_deleted = False
        subcategory.save() 
        messages.success(request, 'subcategory Restored')
    except:
        messages.error(request, 'subcategory does not exist')
        
    return redirect('admin_category')
     
def add_images(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        images = request.FILES.getlist('images')
        color = request.POST.get('color')
        
        for image in images:
            images = ProductImages.objects.create(
                product= product,
                image = image,
                color = color,
                
            )
        return redirect('product_list')

    context = {
        'product': product,
    }

    return render(request, 'upload_images.html', context)


def view_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    category = product.category
    product_type = category.category_name.upper()
    related_images = ProductImages.objects.filter(product=product)

    if product_type == 'PC':
        form_class = PcForm
    elif product_type == 'MONITOR':
        form_class = MonitorForm
    elif product_type == 'KEYBOARD':
        form_class = KeyboardForm
    elif product_type == 'HEADPHONE':
        form_class = HeadphoneForm
    else:
        messages.ERROR(request, 'Product Category does not Exist')
        return redirect('product_list')

    
    form = form_class(instance=product)
    product_fields = {field.name: getattr(product, field.name) for field in Product._meta.fields}
    
    context = {
        "form": form,
        "product": product,
        'product_fields': product_fields,
        "related_images" : related_images,
    }
    return render(request, "adminproductpage.html", context)

@never_cache
@custom_login_required_with_message
def customer_profile(request, pk):
    user = Custom_User.objects.get(id=pk)
    
    context = {
        "user": user,
    }
    return render(request, "shop_customer_profile.html", context)


# Wishlist
@never_cache
@custom_login_required_with_message
def view_wishlist(request):
    user_wishlist = Wishlist.objects.filter(user=request.user)
     
    context = {
        "user_wishlist" : user_wishlist,
    }
    
    return render(request, "shop_customer_wishlist.html", context)
    
@never_cache
@custom_login_required_with_message
def add_to_wishlist(request, pk):
    if request.method == "POST":
        pass
       
        
    else:
        product = Product.objects.get(id=pk)
        if request.user.is_anonymous:
            request.session['wishlist_product_id'] = pk
            messages.info(request, 'You need to log-in first')
            return redirect("userLogin")
        else:
            user = request.user
      
        
        # Check if the product is already in the user's wishlist
        if Wishlist.objects.filter(user=user, product=product).exists():
            # message to display to the user
            messages.info(request, 'Product already in wishlist')
        else:
            # Create a new wishlist entry for the product
            Wishlist.objects.create(user=user, product=product)
            
        
    # Retrieve the user's wishlist
    user_wishlist = Wishlist.objects.filter(user=request.user)
      
    context = {
        "user_wishlist" : user_wishlist,
    }
    
    return render(request, "shop_customer_wishlist.html", context)

@never_cache
@custom_login_required_with_message
def remove_wishlist_item(request, pk):
    user_wishlist = Wishlist.objects.filter(user=request.user)
    product = Product.objects.get(id=pk)
    
    item_to_remove = Wishlist.objects.filter(product=product)
    item_to_remove.delete()
    messages.info(request, 'Product removed from Wishlist')
    
    
    return redirect("view_wishlist")
    
# cart
@never_cache
@custom_login_required_with_message
def view_cart(request):
    items = []
    item = {}
    user = request.user
    cart = Cart.objects.filter(user=user)

    amount = 0
    cart_product = [p for p in Cart.objects.all() if p.user == user]   

    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.discount_price)
            amount+= tempamount
            
    context = {
        "cart" : cart,
        "amount" : amount,     
    } 
    return render(request, "shop_customer_cart.html", context)

@never_cache
@custom_login_required_with_message
def add_to_cart(request, pk):
    
    product = Product.objects.get(id=pk)
    user = request.user
    
    # Check if the product is already in the user's cart
    if Cart.objects.filter(user=user, product=product).exists():
        # message to display to the user
        # instead increment product quantity +=1
        messages.info(request, 'Product already in Cart')
    else:
        # Create a new cart entry for the product
        Cart.objects.create(user=user, product=product)
                  
    return redirect("view_cart")

def plus_cart(request):
    items = []
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.quantity+=1
        c.save()
        TTl_per_price = c.quantity * c.discount_price
        amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user] 
        for p in cart_product:
            # per = p.product.offer.discount_percentage
            tempamount = (p.quantity * p.discount_price)
            amount+= tempamount
            
        data= {
            "quantity" : c.quantity,
            "amount" : amount,
            
        }
        return JsonResponse(data)
             
def minus_cart(request):
    items = []
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.quantity-=1
        if c.quantity < 1:
            c.quantity = 1
        c.save()
        amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user] 
        for p in cart_product:
            # per = p.product.offer.discount_percentage
            tempamount = (p.quantity * p.discount_price)
            amount+= tempamount
            
        data= {
            "quantity" : c.quantity,
            "amount" : amount,
        }

        return JsonResponse(data)
             
def remove_cart(request):
    
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.delete()
        amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user] 
        for p in cart_product:
            # per = p.product.offer.discount_percentage
            tempamount = (p.quantity * p.product.price)
            amount+= tempamount
            # item = {'product': p.product, 'perProductTotal': tempamount}  # Create a new dictionary for each item
            # items.append(item)
            
        data= {
            "amount" : amount,
        }
        
        return JsonResponse(data)


def add_profile_img(request):
    context = {}
    
@never_cache 
def edit_user_profile(request):
    user = request.user
    if request.method == "GET":
        form = CreateUserForm(data=request.user)
        edit = True
    
        
    if request.method == "POST":
        user = request.user
        phone = request.POST.get('phone')
        name = request.POST.get('username')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        
        if email is not None:
            user.email = email
        if phone is not None:
            user.phone = phone
        if name is not None:
            user.username = name
        if image is not None:
            user.image = image
        
        user.save()
        edit = False
        
        
    context = {
        "user" : user,
        "edit": edit,
    }    
           
    return render(request, "shop_customer_profile.html", context)

@never_cache
@custom_login_required_with_message
def customer_adressView(request):
    form = AddressForm()
    user = request.user
    addresses = Address.objects.filter(user=user, is_removed=False)
   
    context = {
        "form" : form,
        "addresses" : addresses,  
    }
    return render(request, "shop_customer_adress.html", context)

      
@never_cache
@custom_login_required_with_message      
def customer_add_address(request):
    addresses = Address.objects.filter(user=request.user , is_removed=False)
   
    if request.method == "POST":
        
        form = AddressForm(request.POST)
     

        if form.is_valid():
            form.save()

            return redirect('customer_adress')
        else:
            print(form.errors)

    else:
        form = AddressForm()  

    context = {
        "addresses": addresses,
        "form": form,
    }
    return render(request, "shop_customer_adress.html", context)


@never_cache
@custom_login_required_with_message
def checkout(request):
    user=request.user
    try:
        user_wallet = Wallet.objects.get(user=user)
        has_wallet = True
    except:
        has_wallet = False
    addresses = Address.objects.filter(user=user, is_removed=False)
    cart_items = Cart.objects.filter(user=user)
    amount = 0
    shipping_cost = 250
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    categories = []
    category_offers = []
    if cart_product: 
        for p in cart_product:
            tempamount = (p.quantity * p.discount_price)
            amount+= tempamount
            categories.append(p.product.category)
        total = amount + shipping_cost
    if len(categories) > 0:
        try:
            for category in categories:
                category_offers.append(Category_offer.objects.get(Q(category=category) & Q(is_active=True)))
        except:
            pass
        print("category offers : ",category_offers)    
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith("product_") and key.endswith("_quantity"):
                product_id = key.split("_")[1]  # Extract the product ID
                quantity = int(value)  # Extract the quantity
                product = Product.objects.get(id=product_id)
                cart = Cart.objects.get(user=request.user, product=product)
                cart.quantity = quantity
       
        # You can perform further actions and redirects here
    context = {
        "addresses" : addresses,
        "amount" : amount,
        "cart_items": cart_items,
        "total" : total,
        "has_wallet" : has_wallet,
        "category_offers" : category_offers,
    }
    return render(request, 'shop_customer_checkout.html', context)

def payment_done(request):
    
    user = request.user
    custid = request.GET.get('custid')
    cart = Cart.objects.filter(user=user)
    
    
    payment_method = request.GET.get('payment_method', '')
    print("Selected payment method is : ", payment_method)
    
    if payment_method not in ['COD', 'PayPal', "wallet"]:
        messages.warning(request, "Please Select a payment method")
        return redirect('checkout')
    
    if custid:
        # A selected address is chosen
        address = Address.objects.get(id=custid)
        print("address selected form list")
    else:
        form = AddressForm(request.GET)
        
        if form.is_valid():
            address = form.save()  
            print("New address created")
        else:
            messages.warning(request, "Address required")
            return redirect('checkout')
        
            
    amount = 0
    shipping_cost = 250
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product: 
        for p in cart_product:
            tempamount = (p.quantity * p.discount_price)
            amount+= tempamount
        total = amount + shipping_cost
        
    coupon_id = request.session.get('coupon_id')
    if coupon_id is not None:
        try:
            coupon = Coupons.objects.get(pk=coupon_id)
            discount = coupon.discount_amount
            total-=discount
            coupon.save()
            del request.session['coupon_id']
        except Coupons.DoesNotExist:
            coupon = None
    
    # take payment from the wallet
    if payment_method == "wallet":
        customer_wallet = Wallet.objects.get(user=user)
        print("customer_wallet.balance before : ",customer_wallet.balance)
        if customer_wallet.balance > total:
            customer_wallet.balance-=total
            customer_wallet.save()
            print("customer_wallet.balance After : ",customer_wallet.balance)

            transaction = Transaction.objects.create(wallet=customer_wallet, amount=total, transaction_type="withdrawal", transaction_balance = customer_wallet.balance )
            coupon.is_used = True
            messages.info(request, "Cash is debited from your Wallet")
        else:
            messages.info(request, "Sorry! Insufficient funds in your Wallet")
            return redirect('checkout')
        
        
    
    
    print("total before placing order : ", total)
    
    order = Orders(user=user, shipping_address=address, billing_address=address, total_amount=total, payment_method=payment_method)
    order.save()
    purchase_cost = total
    coupon = Coupons.create_coupon(purchase_cost)
    
    user_coupon = UserCoupons(user=user, coupon=coupon)
    user_coupon.save()
            
    created_order_items = []
    for c in cart:
        order_item = OrderItems(user=user, order=order, product=c.product, quantity=c.quantity)
        order_item.save()
        created_order_items.append(order_item)
        product=c.product
        product.stock_quantity-=c.quantity
        product.save()
        c.delete()
    
    # Store the order and created order items in the session to pass to the orderconfirmation view
    request.session['order_id'] = order.id
    request.session['created_order_items'] = [item.id for item in created_order_items]
    
    # sent reward to the referer if any
    try:
        print("inside referal reward")
        user_profile = ReferenceProfile.objects.get(user=user)
        print("user profile : ", user_profile)
        print("user profile recomended by : ", user_profile.recommended_by)
        print("user profile : ", user_profile.first_purchase)
        if user_profile.recommended_by is not None and user_profile.first_purchase == 'not_fulfilled':
            referer = user_profile.recommended_by
            try:
                user_wallet = Wallet.objects.get(user=referer)
                reward = Decimal(str(order.total_amount)) * Decimal('0.05')
                if reward > 1000:
                    reward = Decimal(1000)
                user_wallet.balance+=reward
                user_wallet.save()
                transaction = Transaction.objects.create(wallet=user_wallet, amount=reward, transaction_type="deposit", transaction_balance = user_wallet.balance )
            except:
                print("creating new wallet")
                user_wallet = Wallet.objects.create(user=user, balance=0)
                reward = Decimal(str(order.total_amount)) * Decimal('0.05')
                if reward > 1000:
                    reward = Decimal(1000)
                user_wallet.balance+=reward
                user_wallet.save()
                transaction = Transaction.objects.create(wallet=user_wallet, amount=reward, transaction_type="deposit", transaction_balance = user_wallet.balance )
                
            user_profile.first_purchase = 'fulfilled'
            user_profile.save()
            print("first purchace status : ",user_profile.first_purchase)
        else:
            print("no referer")
    except Exception as e:
        print("An exception occurred while updating the wallet:", e)
        pass          

    return redirect("order_confirmation")

@never_cache
@custom_login_required_with_message
def order_confirmation(request):
    # retreving data from the sessions
    order_id = request.session.get('order_id')
    order = Orders.objects.get(id=order_id)
    
    ids = request.session.get('created_order_items')
    created_order_items = OrderItems.objects.filter(id__in=ids)
    
    subtotal = 0
    amount = 0
    shipping_cost = 250
    if created_order_items: 
        for p in created_order_items:
            amount+= p.total_cost
        subtotal = amount + shipping_cost
    context = {
        'order': order,
        'created_order_items': created_order_items,
        "subtotal" : subtotal,
        "amount" : amount,
    }
    return render(request, "shop_confirmation.html", context)

@never_cache
@custom_login_required_with_message
def orders(request):
    user = request.user
    orders = Orders.objects.filter(user=user).order_by('-order_date')
    order_items_list = []
    
    for order in orders:
        order_items = order.orderitems_set.all()
        n = get_status(order.status)
        if n == 0:
            color = 'red'
        elif n == 5:
            color = 'green'
        else:
            color = 'orange'
        order_items_list.append([order, order_items, color])
    
       
    context = {
        "order_items_list" : order_items_list,
    }
    return render(request, "shop_customer_orders.html", context)

@never_cache
@custom_login_required_with_message
def order_details(request, pk):
    order = Orders.objects.get(id=pk)
    created_order_items = order.orderitems_set.all()
    order_total = order.total_amount - 250
    status_str = order.status
    status_completed = get_status(status_str)
    status_pending = 5 - status_completed
    
    completed_steps = [1] * status_completed
    pending_steps = [1] * (5 - status_completed)
    delivered = False
    if status_completed == 5:
        delivered = True
    print(delivered)
    context = {
        "order" : order,
        "created_order_items" : created_order_items,
        "order_total" : order_total,
        "completed_steps" : completed_steps,
        "pending_steps" : pending_steps,
        "delivered" : delivered,
    }
    return render(request, "shop_customer_order_details.html", context)

@custom_login_required_with_message
def cancel_order(request , pk):
    try:
        customer_wallet = Wallet.objects.get(user = request.user)
    except:
        customer_wallet = None
    if customer_wallet is not None:
        order = Orders.objects.get(id=pk)
        order.status = "Cancelled"
        order.save()
        
        if order.payment_method != "COD":
            refund_amount = order.total_amount
            
            customer_wallet.balance+=refund_amount
            customer_wallet.save()

            transaction = Transaction.objects.create(wallet=customer_wallet, amount=refund_amount, transaction_type="deposit", transaction_balance = customer_wallet.balance )
            
            messages.info(request, "Cash is refunded to your Wallet")
        else:
            messages.info(request, "Order Cancelled ")
        return redirect("orderDetails", pk)
    else:
        # messages.info(request, "You need to create a Wallet First")
        request.session['for_refunding'] = True
        request.session['order_id'] = pk
        
        return redirect("new_wallet")
        

def forgot_password(request):
    context = {}
    return render(request, "shop_forgot_password.html", context)

def send_otp_email(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user = Custom_User.objects.filter(email=user_email)
        if not user:
            messages.error(request, "No such user.\nPlease enter a valid Email.")
            return redirect("forgot_password")
        
        request.session['email'] = user_email
        otp = send_otp(request)
        subject = 'Password Reset OTP'
        message = f'Your OTP for password resetting is {otp}'
        send_email_to_client(subject, message, user_email)
        
        return render(request, 'shop_otp_verification.html')
        
    return render(request, "shop_forgot_password.html")

def veryify_email_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']
        
        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)
            
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    return redirect("password_reset")
                else:
                    messages.info(request,'invalid OTP')
            else:
                messages.info(request,'OTP Expired')
        else:
            messages.info(request,'Someting went wrong try again')
        return redirect("forgot_password")
    
def password_reset(request):
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 == password2:
            email = request.session['email']
            try:
                if email is not None:
                    user = Custom_User.objects.get(email=email)
                else:
                    user = request.user
            except:
                messages.error(request, "Sorry! something went wrong.")
                return redirect("forgot_password")
            user.set_password(password1)
            user.save()
            return redirect("userLogin")
       
    context={}
    return render(request, "shop_password_reset.html", context)

@never_cache
@custom_login_required_with_message
def edit_address(request, pk):
    address = Address.objects.get(id=pk)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)  
        if form.is_valid():
            form.save() 
            return redirect('customer_adress')
    else:
        form = AddressForm(instance=address)
    context = {
        'form' : form,
        "edit" : True,
        "id" : pk,
    }
    return render(request, "shop_customer_adress.html", context)


@custom_login_required_with_message
def remove_address(request, pk):
    address = Address.objects.get(id=pk)
    address.is_removed = True
    address.save()
    return redirect("customer_adress")

@never_cache
@custom_login_required_with_message
def return_order(request, pk):
    order_items = OrderItems.objects.get(id=pk)
    if request.method == "POST":
        form = ReturnForm(request.POST)
        if form.is_valid():
            return_request = form.save(commit=False)
            return_request.order = order_items.order
            return_request.product = order_items.product
            return_request.status = 'Pending'  # Set an initial status
            return_request.save()
            order_items.is_returned = True
            order_items.save()
            order = Orders.objects.get(id= order_items.order.id)
            order.status = "Returned"
            order.save()
            # refund the amount to the customer wallet
            if order.payment_method != "COD":
                try:
                    customer_wallet = Wallet.objects.get(user = request.user)
                except:
                    customer_wallet = None
                if customer_wallet is not None:
                    refund_amount = return_request.value
                    customer_wallet.balance+=refund_amount
                    customer_wallet.save()
                    transaction = Transaction.objects.create(wallet=customer_wallet, amount=refund_amount, transaction_type="deposit", transaction_balance = customer_wallet.balance )
            
                    messages.info(request, "Cash is refunded to your Wallet")
                
                return render(request,'return_success_page.html')
            else:
                messages.info(request, "Return request has been submitted")
                return render(request,'return_success_page.html')
                
        else:
            print(form.errors)
    form = ReturnForm()
    context = {
        "order_items" : order_items,
        "form" : form,
    }
    return render(request, "shop_customer_return.html", context)

@never_cache
def product_return_status(request, pk):
    order_item = OrderItems.objects.get(id=pk)
    order = Orders.objects.get(id=order_item.order.id)
    returned = Return.objects.filter(order=order)
    context = {
        "order_item" : order_item,
        "returned" : returned,
        "order" : order,
    }
    return render(request, "shop_customer_return_status.html", context)

    

def admin_orders_list(request):
    orders = Orders.objects.all()
    pending = Orders.objects.filter(status='Processing')
    confirmed = Orders.objects.filter(status='Confirmed')
    delivered = Orders.objects.filter(status='Delivered')
    cancelled = Orders.objects.filter(status='Cancelled')
    
    status_counts = {
        'Pending': len(pending),
        'Confirmed': len(confirmed),
        'Delivered': len(delivered),
        'Cancelled': len(cancelled),
        'All_order_count' : len(orders),
    }
    print('Pending : ', len(pending), 'Confirmed : ', len(confirmed), 'Delivered : ', len(delivered), 'Cancelled : ', len(cancelled))
    context = {
        'status_counts': status_counts,
        'pending_orders': pending,
        'confirmed_orders': confirmed,
        'delivered_orders': delivered,
        'cancelled_orders': cancelled,
        'orders' : orders,
    }
    return render(request, "admin_orders_view.html", context)

def admin_change_order_status(request, pk):
    if request.method == 'POST':
        order = Orders.objects.get(id=pk)
        status = request.POST.get('status')
        order.status = status
        order.save()
        messages.info(request, 'Stutus Updated Succefully')
    return redirect("admin_orders_list")

def admin_inventory_list(request):
    products = Product.objects.all()
    context = {
        "products" : products,
    }
    return render(request, "admin_inventory.html", context)

def admin_add_product_stock(request, pk):
    if request.method == "POST":
        product = Product.objects.get(id=pk)
        qty = int(request.POST.get('quantity'))
        product.stock_quantity+=qty
        product.save()
        return redirect('admin_inventory_list')

@never_cache  
def product_category(request):
    products = Product.objects.all()
    search_query = request.GET.get('q', '')
    brands = Brand.objects.all()
    category_offer = None
    if request.method == "POST":
        choice_name = request.POST.get("choice")
        choice_subcategory = get_object_or_404(SubCategory, name=choice_name)
        products = Product.objects.filter(subcategories=choice_subcategory)
        
        try:
            category_offer = Category_offer.objects.filter(Q(category=choice_subcategory.category) & Q(is_active=True))
        except Category_offer.DoesNotExist:
            category_offer = None
        except Exception as error:
            print("An error occurred:", error)
            
    if search_query:
        products = Product.objects.filter(product_name__icontains=search_query,)
    
    

    paginator = Paginator(products, 12) 
    # Get the current page number from the request's GET parameter
    page_number = request.GET.get('page')
    # Get the Page object for the current page number
    page = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_deleted=False)
    cat_data = []

    for category in categories:
        subcategories = SubCategory.objects.filter(category=category, is_deleted=False)
        cat_item = {
            'category': category,
            'subcategories': subcategories,
            
        }
        cat_data.append(cat_item)
        
    colors = []
    for product in products:
        color = product.color
        if color not in colors:
            colors.append(color)

    context = {
        'cat_data': cat_data,
        'products' : page,
        "brands" : brands,
        "colors" : colors,
        "category_offer" : category_offer,
    }
    print("Category offer is : ", category_offer)
    return render(request, "shop_product_category.html", context)


from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.db import models
from django.core.files.storage import default_storage


@require_POST
def filter_products(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        selected_brands = request.POST.getlist("brands[]")
        selected_colors = request.POST.getlist("colors[]")
        lower_price = float(request.POST.get("lower_price"))
        upper_price = float(request.POST.get("upper_price"))

        print("Brand : ", selected_brands, "color : ", selected_colors, "Price range : ", lower_price, " : ", upper_price)

        products = Product.objects.all()

        # Filter based on selected_colors (if any)
        if selected_colors:
            products = products.filter(color__in=selected_colors)
            print("filtered colors : ",products)

        # Filter based on selected_brands (if any)
        if selected_brands:
            brands = Brand.objects.filter(brand_name__in=selected_brands)
            products = products.filter(brand__in=brands)
            print("filtered brands : ",products)


        # Filter based on price range
        products = products.filter(price__gte=lower_price, price__lte=upper_price)
        print("final Products : ",products)


        filtered_products_data = list(products.values())

        for product in filtered_products_data:
            product['price'] = float(product['price'])
            product['product_detail_url'] = reverse('product_detail', args=[product['id']])
            image_url = '/media/{}'.format(product['image'])
            product['image_url'] = image_url
            

            # Construct URLs for add-to-cart and add-to-wishlist
            product['add_to_cart_url'] = reverse('add_to_cart', args=[product['id']])
            product['add_to_wishlist_url'] = reverse('add_to_wishlist', args=[product['id']])
        

        # Return the filtered products as JSON response
        return JsonResponse({'filtered_products': filtered_products_data})

    return JsonResponse({'error': 'Invalid request'})


@never_cache
@custom_login_required_with_message    
def view_coupons(request):
    user = request.user
    user_coupons = UserCoupons.objects.filter(user=user)

    # Create a list to store the details of associated coupons
    coupon_details = []

    for user_coupon in user_coupons:
        coupon = user_coupon.coupon  # Access the associated coupon
        if not coupon.is_used:
            coupon_details.append({
                'coupon_code': coupon.coupon_code,
                'discount_amount': coupon.discount_amount,
                'expiration_date': coupon.expiration_date,
            })

    context = {
        "user_coupons": coupon_details,
    }
    return render(request, "shop_customer_coupons.html", context)

def admin_offers(request, pk=None):
    form = MainOfferForm()
    if request.method == "POST":
        offers = Offers.objects.all()
        for offer in offers:
            offer.is_active = False
            offer.save()
        selected_offer = Offers.objects.get(id=pk)
        selected_offer.is_active = True
        selected_offer.save()
        
    offers = Offers.objects.all()
    context = {
        "offers": offers,
        "form" : form,
    }
    return render(request, "admin_offers.html", context)

def add_admin_offers(request):
    if request.method == "POST":
        form = MainOfferForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('admin_offers')
    else: 
        print("Not PoST")

def delete_offer(request, pk):
    offer = Offers.objects.get(id=pk)
    offer.delete()
    return redirect('admin_offers')

import json

def validate_coupon(request):
    coupon_code = request.GET.get('coupon_code')
    
    try:
        coupon = Coupons.objects.get(coupon_code=coupon_code)
    except Coupons.DoesNotExist:
        response_data = {
            'error': 'Coupon not found',
        }
        return JsonResponse(response_data, status=400)
    except Exception as e:
        response_data = {
            'error': 'An error occurred while validating the coupon.',
        }
        return JsonResponse(response_data, status=500)
    
    discount = None
    message = None
    
    if coupon is not None:
        now = timezone.now().date()  # Convert to date
        if not coupon.is_used and coupon.expiration_date > now:
            discount = coupon.discount_amount
            request.session['coupon_id'] = coupon.id
            # request.session['discount'] = discount
        elif coupon.is_used:
            message = "Sorry! the coupon is already used"
        else:
            message = "Coupon expired"
    else:
        message = "Invalid coupon"
    
    response_data = {
        'discount': discount,
        "message" : message,
    }
    
    return JsonResponse(response_data)

def admin_brand(request):
    brands = Brand.objects.all()
    context = {
        "brands" : brands,
    }
    return render(request, "admin_brand_view.html", context)

def edit_brand(request, pk):
    brand = Brand.objects.get(id=pk)
    if request.method == "POST":
        name = request.POST['brand_name']
        brand.brand_name = name
        brand.save()
        return redirect("admin_brand")
    context = {
        "brand": brand
    }
    return render(request, "admin_brand_edit.html", context)

def add_review(request, pk):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        message = request.POST.get('message')
        product = Product.objects.get(id=pk)
        review = Reviews.objects.create(user=request.user, product=product, review_text=message, rating= rating )
        
        print(review)
        return redirect('product_detail', pk)
