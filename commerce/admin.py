from django.contrib import admin

from commerce.models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    def observation(self, instance):
        if int(instance.qty_commanded) >= instance.moq:
            return 'La MOQ est atteinte'
        else:
            return 'attente d\' atteinte de MOQ'
     
    list_display = ('name', 'category', 'short_desc', 'price', 'date_validity', 'moq', 'qty_commanded', 'observation')
    date_hierarchy = 'date_validity'
    list_filter = ('category', 'date_added',)
    ordering = ('name',)
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    def total(self, instance):
        return instance.total()
    
    def apercu_type(self, order):
        return order.address.type
    
    apercu_type.short_description = 'Type'
    
    list_display = ('order_date', 'user', 'apercu_type', 'address', 'total')
    date_hierarchy = 'order_date'
    list_filter = ('user', 'address')

class OrderSpecialAdmin(admin.ModelAdmin):        
    list_display = ('order_date', 'name', 'short_desc')
    date_hierarchy = 'order_date'
#     list_filter = ('user', 'address')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderSpecial, OrderSpecialAdmin)