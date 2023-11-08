from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.userLogin, name="userLogin"),
    path("signup/", views.userSignup, name="userSignup"),
    path("logout/", views.userLogout, name="userLogout"),
    path("otp/", views.otpview, name="otp"),
    path("resend_otp/", views.resend_otp, name="resend_otp"),
    path("product_detail/<int:pk>/", views.product_detail, name="product_detail"),
    path("product_detail/<int:pk>/<str:clr>", views.product_detail, name="product_detail"),
    
    
    path("demo/", views.demo, name="demo"),
    path('adminlogin/', views.admin_login, name='adminlogin'),
    path('admindashboard/', views.admin_dashboard, name='admin_dashboard'),
    path("user_status/<str:pk>/", views.userstatus, name="user_status"),
    path("adminlogout/", views.adminLogout, name="admin_logout"),
    path("admincategory/", views.adminCategoryManagement, name="admin_category"), 
    path('productlist/', views.product_list, name='product_list'),
    path('addproduct/', views.add_product, name='add_product'),
    path('addnewproduct/<int:pk>/', views.add_new_product, name='add_new_product'),
    path('editproduct/<int:pk>/', views.edit_product, name='edit_product'),
    path('deleteproduct/<int:pk>/', views.delete_product, name='delete_product'),
    path('includedDelItems/', views.soft_deleted, name='included_del_items'),
    path('searchProducts/', views.product_list, name='search_products'),
    
    # categories
    path('editcategory/<int:pk>/', views.edit_category, name='editCategory'),
    path('deletecategory/<int:pk>/', views.delete_category, name='deleteCategory'),
    path('subcategory/<int:pk>/', views.sub_category, name='subCategory'),
    path('editsubcategory/<int:pk>/', views.edit_sub_category, name='editsubCategory'),
    # path('addsubcategory/<int:pk>/', views.add_sub_category, name='add_sub_category'),
    
    path('addsubcategory/', views.add_sub_category, name='add_sub_category'),
    path('addsubcategory/<int:pk>/', views.add_sub_category, name='add_sub_categorynew'),
    path('addsubcategory/<int:pk>/', views.edit_sub_category, name='edit_sub_category'),
    path('delsubcategory/<int:pk>/', views.delete_sub_category, name='deletesubCategory'),
    
    # multiple images
    path('addimages/<int:pk>/', views.add_images, name='add_images'),  
    path('viewproduct/<int:pk>/', views.view_product, name='view_product'),
    
    # shop user
    path('customerprofile/<int:pk>/', views.customer_profile, name='customer_profile'),
        
    # wishlist  
    path('add_to_wishlist/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('view_wishlist/', views.view_wishlist, name='view_wishlist'),
    path('remove_from_wishlist/<int:pk>/', views.remove_wishlist_item, name='remove_wishlist_item'),
    
    # cart
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    # path('remove_from_cart/<int:pk>/', views.remove_cart_item, name='remove_cart_item'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),    
    path('removecart/', views.remove_cart, name='removecart'),

    # customer
    
    path('add_profile_img/', views.add_profile_img, name='add_profile_img'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),

    path('includedDelCat/', views.view_deleted_categories, name='included_del_cat'),
    path('restoreCategory/<int:pk>/', views.restoreCategory, name='restoreCategory'),
    path('includedDelSubCat/', views.view_deleted_subcategories, name='included_del_subcat'),  
    path('restoreSubCategory/<int:pk>/', views.restoreSubCategory, name='restoreSubCategory'),
    
    
    
    path('edit_address/<int:pk>/', views.edit_address, name='edit_address'),

    
    path('customer_adress/', views.customer_adressView, name='customer_adress'),
    path('add_adress/', views.customer_add_address, name='add_address'),
    path('remove_address/<int:pk>/', views.remove_address, name='remove_address'),
    
    # checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('paymentDone/', views.payment_done, name='paymentDone'),
    
    # orders
    path('orders/', views.orders, name='orders'),
    path('orderDetails/<int:pk>/', views.order_details, name='orderDetails'),
    path('cancel_order/<int:pk>/', views.cancel_order, name='cancel_order'),
    path('return_order/<int:pk>/', views.return_order, name='return_order'),
    path('product_return_status/<int:pk>/', views.product_return_status, name='product_return_status'),
    
      
      
    # reset password
    path('send_otp_email/', views.send_otp_email, name='send_otp_email'),
    path('veryify_email_otp/', views.veryify_email_otp, name='veryify_email_otp'),
    path('password_reset/', views.password_reset, name='password_reset'),
    
    # admin orders
    path('admin_orders_list/', views.admin_orders_list, name='admin_orders_list'),
    path('change_order_status/<int:pk>/', views.admin_change_order_status, name='change_order_status'),
    
    # admin inventory
    path('admin_inventory_list/', views.admin_inventory_list, name='admin_inventory_list'),
    path('add_product_stock/<int:pk>/', views.admin_add_product_stock, name='add_product_stock'),
    
    # category
    path('product_category/', views.product_category, name='product_category'),
    path('update_product_filter/', views.filter_products, name='product_filter'),
    path('select_category/', views.product_category, name='select_category'),
     
    # coupons
    path('view_coupons/', views.view_coupons, name='view_coupons'),
    path('validate_coupon/', views.validate_coupon, name='validate_coupon'),
    
    # offer management
    path('admin_offers/', views.admin_offers, name='admin_offers'),
    path('admin_offers/<int:pk>/', views.admin_offers, name='admin_offers'),
    path('add_admin_offers/', views.add_admin_offers, name='add_admin_offers'),
    path('delete_offer/<int:pk>/', views.delete_offer, name='delete_offer'),
    
    
    # brand management
    path('admin_brand/', views.admin_brand, name='admin_brand'),
    path('edit_brand/<int:pk>/', views.edit_brand, name='edit_brand'),
    
    # rating
    path('add_review/<int:pk>/', views.add_review, name='add_review'),
    
    # invoice PDF
   

    
    

]