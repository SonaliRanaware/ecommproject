from django.contrib import admin

from .models import product
from .models import Cart,Order
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
      list_display=['id','name','price','pdetails','cat','is_active','pimage']
      list_filter=['cat','is_active']
class CartAdmin(admin.ModelAdmin):
      list_display=['id','uid','pid']    
class OrderAdmin(admin.ModelAdmin):
      list_display=['id','order_id','uid','pid']         
admin.site.register(product,ProductAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Order,OrderAdmin)

