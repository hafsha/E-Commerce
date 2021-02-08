from django.contrib import admin
from store.models import Customer, Product, Order, OrderItem, ShippingAddress
# Register your models here.


admin.site.register(Product)



class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','complete', 'customer','date_ordered',  'transaction_id')

admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer','order')

    def customer(self,obj):
        if obj.order:
            return  obj.order.customer.name
        return 'No  Order  Found'
admin.site.register(OrderItem,  OrderItemAdmin)

admin.site.register(ShippingAddress)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','email')

admin.site.register(Customer,CustomerAdmin)