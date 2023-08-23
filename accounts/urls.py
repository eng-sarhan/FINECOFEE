from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),

    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('product_favorite/<int:pro_id>', views.product_favorite, name='product_favorite'),
    path('show_product_favorite/', views.show_product_favorite, name='show_product_favorite'),

]
