from django.contrib import admin
from .models import Product, Category, Company


class ProductAdmin(admin.ModelAdmin):
    list_display=('name','description','price','photo','is_active','publish_date')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Company)
