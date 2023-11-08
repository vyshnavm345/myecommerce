from django.urls import path
from . import views

urlpatterns = [
    path("", views.wallet_view, name="wallet_view"),
    path("new_wallet/", views.new_wallet, name="new_wallet"),
    path("deposit_wallet/", views.deposit_wallet, name="deposit_wallet"),
]