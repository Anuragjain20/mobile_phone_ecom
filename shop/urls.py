from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('show_all_phones/', show_all_phones, name='show_all_phones'),
    path('product_details/<int:id>/', product_details, name='product_details'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart, name='cart'),
    path('orders/payment-successfull/', payment_successfull, name='payment_successfull'),
]
