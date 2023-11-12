from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.db import models
import datetime
import secrets
import random
import string


def generate_coupon_code():
    # Generate a random coupon code of 10 characters
    coupon_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return coupon_code

def calculate_expiration_date():
    # Calculate the expiration date as 30 days from the current date
    return timezone.now() + timezone.timedelta(days=30)


class Custom_User(AbstractUser):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Blocked', 'Blocked'),
    ]
    email = models.EmailField(unique=True)  # Make the email field unique
    status = models.CharField(default="Active", max_length=20, null=True, blank=True, choices=STATUS_CHOICES)
    image = models.ImageField(upload_to='uploads/users/', null=True, blank=True)
    phone = models.CharField(max_length=14,  null=True, blank=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user_set')
    
    def __str__(self):
        return self.username

  
class Address(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.DO_NOTHING)
    name = models.CharField( max_length=200, blank= True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20 ,null=True, blank=True)
    is_removed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"
        
    def __str__(self) -> str:
        return f"Name : {self.user}\nStreet : {self.street_address}\nCity : {self.city}\nState : {self.postal_code}\nCountry : {self.country}\nPhone : {self.phone_number}"
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.user.username
        super(Address, self).save(*args, **kwargs)


class Coupons(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Coupons"
        
    @classmethod
    def create_coupon(cls, purchase_cost):
        purchase_cost_float = float(purchase_cost)
    
        # Calculate the discount amount using a float
        discount_amount = max(purchase_cost_float * 0.05, 100)
        
        # Generate a unique coupon code
        coupon_code = generate_coupon_code()

        # Calculate the expiration date
        expiration_date = calculate_expiration_date()

        # Create a new coupon object
        coupon = cls(
            coupon_code=coupon_code,
            discount_amount=discount_amount,
            expiration_date=expiration_date
        )
        coupon.save()  # Save the coupon to the database

        return coupon
    def __str__(self) -> str:
        return self.coupon_code

class UserCoupons(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "User Coupons"
    def __str__(self) -> str:
        return self.user.username

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    verified = models.BooleanField(default=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self) -> str:
        return self.category_name    



class Offers(models.Model):
    offer_name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name_plural = "Offers"
    def __str__(self) -> str:
        return self.offer_name


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product_is_deleted=False)

class SoftDeletedProducts(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product_is_deleted=True)

class  Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField()
    color = models.CharField(max_length=50)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subcategories = models.ManyToManyField("SubCategory", blank=True)
    image = models.ImageField(upload_to='uploads/product/')
    offer = models.ForeignKey(Offers, on_delete=models.DO_NOTHING, null=True, blank=True)
    product_is_deleted = models.BooleanField(default=False, null=True, blank=True)
    specification = models.TextField(null=True, blank=True)
    
    objects = ProductManager()
    
    removed_products = SoftDeletedProducts()
    
    all_objects = models.Manager()
    
    def __str__(self) -> str:
        return self.product_name
    

# PC Model (inherits from Product)
class Pc(Product):
    ram = models.CharField(max_length=20, null=True, blank=True, choices=[('8' , "8GB"), ('16', "16GB"), ('32', "32GB"), ('64', "64GB")])  
    
    class Meta:
        db_table = 'pc'
    
    def __str__(self) -> str:
        return self.product_name

# Monitor Model (inherits from Product)
class Monitor(Product):
    DISPLAY_OPTIONS = [
        ('18', '18 inch'),
        ('20', '20 inch'),
        ('22', '22 inch'),
        ('24', '24 inch'),
        ('26', '26 inch'),
        ('28', '28 inch'),
        ('30', '30 inch'),
        ('32', '32 inch'),
        ('34', '34 inch'),
        ('36', '36 inch'),
        ('38', '38 inch'),
        ('40', '40 inch'),
        ('42', '42 inch'),
    ]
    display_size = models.CharField(max_length=20, null=True, blank=True, choices=DISPLAY_OPTIONS)
    
    class Meta:
        db_table = 'monitor'  # Name of the database table for Monitors

# Keyboard Model (inherits from Product)
class Keyboard(Product):
    rgb_support = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'keyboard'  # Name of the database table for Keyboards   

class Headphone(Product):
    VARIANT_CHOICES = [
        ('Wired', 'Wired'),
        ('Bluetooth', 'Bluetooth'),
    ]
    headphone_type = models.CharField(max_length=50, null=True, blank=True, choices=VARIANT_CHOICES)
        
    class Meta:
        db_table = 'headphone' # Name of the database table for Keyboards
        
# remember to put others or use base product model for the rest of the products that does not fit this category
       

class Brand(models.Model):
    brand_name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.brand_name   
    

class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product/', null=True, blank=True)
    color = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "Product Images"
    
    def __str__(self) -> str:
        return f"{self.product}-{self.color}"

class Orders(models.Model):
    STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
    ]
    user = models.ForeignKey(Custom_User, on_delete=models.DO_NOTHING)
    username = models.CharField(max_length=150, blank=True)
    shipping_address = models.ForeignKey(Address, related_name='orders_shipping', on_delete=models.SET_NULL, null=True)
    billing_address = models.ForeignKey(Address, related_name='orders_billing', on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(default=datetime.datetime.today)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    tracking_id = models.CharField(max_length=50, blank=True, null=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "ORDERS"
    
    def __str__(self):
        return f"Order for {self.username}"

    def generate_tracking_id(self, length=10):
        characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Generate a random tracking ID of the specified length
        tracking_id = ''.join(secrets.choice(characters) for _ in range(length))

        return tracking_id

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            # Generate a tracking ID only if it doesn't exist
            self.tracking_id = self.generate_tracking_id(10)

        if self.user:
            self.username = self.user.username

        super(Orders, self).save(*args, **kwargs)
    

class OrderItems(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.DO_NOTHING, default=None)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    is_returned = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Order Items"
    
    @property
    def discount_price(self):
        try:
            per = self.product.offer.discount_percentage
            discounted_price = self.product.price - (self.product.price * per / 100)
            return round(discounted_price, 2)  
        except:
            return self.product.price
        
    @property
    def total_cost(self):
        return self.quantity * self.discount_price
    
    def save(self, *args, **kwargs):
        if not self.selling_price:
            self.selling_price = self.total_cost
        super(OrderItems, self).save(*args, **kwargs)
        

class Reviews(models.Model):
    stars = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
        # Add more status options as needed
    ]
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField(choices=stars, default=1)
    review_date = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Reviews"
        
    def __str__(self) -> str:
        return f"{self.user} rated {self.product}" 

class Cart(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    
    @property
    def discount_price(self):
        try:
            per = self.product.offer.discount_percentage
            discounted_price = self.product.price - (self.product.price * per / 100)
            return round(discounted_price, 2)  
        except:
            return self.product.price
    
    @property
    def total_cost(self):
        return self.quantity * self.discount_price
    
    def __str__(self) -> str:
        return f"{self.user}-{self.product}-{self.quantity}"

class Payment(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)

class Shipping(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    shipping_method = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=50)

class Wishlist(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.user}-{self.product}"
    
class Return(models.Model):
    STATUS_CHOICES = {
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
    }
    
    order = models.ForeignKey('Orders', on_delete=models.DO_NOTHING)
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=1)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    return_date = models.DateField(auto_now=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self) -> str:
        return f"{self.order} returned {self.product}"
    
    def save(self, *args, **kwargs):
        # If quantity is not set, set it to the quantity from the related OrderItems
        if not self.quantity:
            self.quantity = self.order.orderitems_set.get(product=self.product).quantity

        super(Return, self).save(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        # If quantity is not set, set it to the quantity from the related OrderItems
        if not self.quantity:
            self.quantity = self.order.orderitems_set.get(product=self.product).quantity

        # Calculate the value based on the quantity and selling_price of the related OrderItems
        order_item = self.order.orderitems_set.get(product=self.product)
        if not self.value:
            self.value = order_item.selling_price

        super(Return, self).save(*args, **kwargs)
        
               
class Category_offer(models.Model):
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
    offer_name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    discount_percentage = models.IntegerField()
    banner = models.ImageField(upload_to='uploads/category/', null=True, blank=True)
    
    
    def __str__(self) -> str:
        return f"{self.offer_name} for {self.category}"
    