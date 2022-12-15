from django.contrib import admin

# Register your models here.
from shop.models import Product
from shop.models import Orders, OrderUpdate
admin.site.register(Product) 
admin.site.register(Orders)
admin.site.register(OrderUpdate)