from django.urls import path
from .import views

urlpatterns = [
    path("customer_referals/", views.customer_referals, name="customer_referals"),
    path("<str:ref_code>/", views.main_view, name="main_view"),
]