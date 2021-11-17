"""ShoppyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shopapp import views as V
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^addnewaddress/$',V.addnewaddress,name='addnewaddress'),
    url(r'^$', V.productinformation, name='product_info'),
    path('home/',V.home, name = 'home'),
    path('product_info/',V.productinformation, name = 'product_info'),
    path('orderproduct/',V.orderproduct, name = 'orderproduct'),
    path('user/registeration/',V.userregister, name = 'register'),
    path('user/login/',V.shoppyLogin, name = 'login'),
    path('user/logout/',V.logout_view, name = 'logout'),
    path('user/display_all_added_prodcuts',V.cart, name = 'cart_all_added_prodcuts'),
    path('user/shopping_cart',V.do_not_need_this_item, name = 'do_not_need_this_item'),
    path('user/update_quantity',V.update_quantity, name = 'update_quantity'),
    path('user/proceedtocheckout',V.proceedtocheckout, name = 'proceedtocheckout'),
    path('user/continue_to_checkout',V.continue_to_checkout, name = 'continue_to_checkout'),
    path('user/continue_to_payment',V.continue_to_payment, name = 'continue_to_payment'),
    path('user/order_confirmation_page_of_the_placed_order',V.order_confirmation_page, name = 'order_confirmation_page'),
    path('user/previous_orders',V.previous_orders, name = 'previous_orders'),
    url(r'^completeorder/$', V.completePayment,name='completePayment'),
    path('user/account_settings',V.account_settings, name = 'account_settings'),
    url(r'^editaddress/$',V.editaddress,name='editaddress'),
    url(r'^deleteaddress/$',V.deleteaddress,name='deleteaddress'),

     
]
