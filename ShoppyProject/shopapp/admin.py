from django.contrib import admin

# Register your models here.
from .models import *

class AdminUI_ItemModel(admin.ModelAdmin):

    list_display = ['itemid','itemname','price','imageUrl','description','label',]
    list_filter = ['price']
    list_search = ('itemname','itemid')
    list_display_links = ('itemname', 'itemid')

    class meta:
        model = ItemModel

     
class AdminUI_UserProfileRegistrationModel(admin.ModelAdmin):
    list_display = ['username','first_name','last_name','email','mobilno','registered_on',]
    list_filter = ['username']
    list_search = ('username')
    list_display_links = ('username',)

    class meta:
        model = UserProfileRegistrationModel

admin.site.register(UserProfileRegistrationModel,AdminUI_UserProfileRegistrationModel)
admin.site.register(ItemModel,AdminUI_ItemModel)
admin.site.register(OrderItemModel)
admin.site.register(OrderModel)
admin.site.register(PaymentModel)
admin.site.register(ShippingAdress)
admin.site.register(BillingAddressModel)



