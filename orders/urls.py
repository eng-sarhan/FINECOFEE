
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name = 'cart'),
    path('remove_from_cart/<int:orderdetails_id>', views.remove_from_cart, name = 'remove_from_cart'),
    path('add_qty/<int:orderdetails_id>', views.add_qty, name = 'add_qty'),
    path('sub_qty/<int:orderdetails_id>', views.sub_qty, name = 'sub_qty'),
    path('chechout/', views.chechout, name = 'chechout'),
    path('my_order/', views.my_order, name = 'my_order'),

]
