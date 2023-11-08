from .models import *
from .forms import *
from django.core.mail import send_mail
from django.conf import settings


# if needed it can also return a list[product_instance, category, product_form_type]  
# this function returns either None or a valid form 
def get_product_form(pk):
    product_inst = Product.objects.get(id=pk)
    category = product_inst.category
    product_type = category.category_name.upper()
   
    form_class = None
    if product_type == 'PC':
        form_class = PcForm
    elif product_type == 'MONITOR':
        form_class = MonitorForm
    elif product_type == 'KEYBOARD':
        form_class = KeyboardForm
    elif product_type == 'HEADPHONE':
        form_class = HeadphoneForm
            
    return form_class


def variants(product_instance):
    lis = {}
    if isinstance(product_instance, Pc):
        # It's a PC, access PC-specific fields
        lis["ram"] = product_instance.ram

    elif isinstance(product_instance, Monitor):
        # It's a Monitor, access Monitor-specific fields
        lis["display_size"] = product_instance.display_size

    elif isinstance(product_instance, Keyboard):
        # It's a Keyboard, access Keyboard-specific fields
        lis["rgb_support"] = product_instance.rgb_support

    elif isinstance(product_instance, Headphone):
        # It's a Headphone, access Headphone-specific fields
        lis["headphone_type"] = product_instance.headphone_type

    return lis  # Return the dictionary with attribute values or an empty dictionary



def variants(product_instance):
    lis = {}
    print(f"Instance type: {type(product_instance)}")  # Print the instance type

    if isinstance(product_instance, Pc):
        # It's a PC, access PC-specific fields
        lis["ram"] = product_instance.ram

    elif isinstance(product_instance, Monitor):
        # It's a Monitor, access Monitor-specific fields
        lis["display_size"] = product_instance.display_size

    elif isinstance(product_instance, Keyboard):
        # It's a Keyboard, access Keyboard-specific fields
        lis["rgb_support"] = product_instance.rgb_support

    elif isinstance(product_instance, Headphone):
        # It's a Headphone, access Headphone-specific fields
        lis["headphone_type"] = product_instance.headphone_type

    return lis  

def get_status(status):
    if   status == 'Processing':
        return 1
    elif status == 'Confirmed':
        return 2
    elif status == 'Shipped':
        return 3
    elif status == 'Out for Delivery':
        return 4
    elif status == 'Delivered':
        return 5
    elif status == 'Cancelled':
        return 0
    else:
        return 5
    
def send_email_to_client(sub, msg, user):
    subject = sub
    message = msg
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user]
    print(subject,  message, from_email, recipient_list)
    send_mail(subject, message, from_email, recipient_list)
