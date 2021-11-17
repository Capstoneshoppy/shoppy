from shopapp.models import ItemModel
from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

def home(request):
    return render(request,'userinterfacefiles/home.html')
# https://docs.djangoproject.com/en/1.8/topics/auth/passwords/#django.contrib.auth.hashers.make_password

# https://stackoverflow.com/questions/20997618/how-to-quickly-encrypt-a-password-string-in-django-without-an-user-model


def userregister(request):
    # username = request.POST['username']
    # dateofbirth= request.POST['date_of_birth']
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobileno = request.POST.get('mobileno')
        password = request.POST.get('password')
        username = str(f_name)+" "+str(l_name)+"-"+str(mobileno)
        try:
            UserProfileRegistrationModel.objects.get(email=email)
            context={'message':'Same email is been using by others, Please change it',
            'first_name':f_name,
            'last_name':l_name,
            'email':email,
            'mobileno':mobileno}
            return render(request,'userinterfacefiles/register.html',context)
        except ObjectDoesNotExist:
            UserProfileRegistrationModel(first_name=f_name,last_name=l_name,username=username,email=email,
            password=make_password(password),mobilno=mobileno).save()
            context={'message':'Account has been created, You can now login'}
            name = f_name+l_name
            subject = 'Welcome Mail from Shoppy'
            message = 'Hello '+name+'\nThank You for registering with us. We make sure you will nicely shopping experience with us\n\n\n\n\n\nRegards\n\nShoppy Admin Team'
            
            email_from =settings.EMAIL_HOST_USER
            recipient_list = [email ]
            send_mail( subject, message, email_from, recipient_list )

            return render(request,'userinterfacefiles/register.html',context)

        
    return render(request,'userinterfacefiles/register.html')

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password

def productinformation1(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            items = ItemModel.objects.all()
            context={'items':items}
            return render(request,'userinterfacefiles/productinformation.html',context)
        else:
            context={'message':'You are not authenticated'}
            return render(request,'userinterfacefiles/register.html',context)
    else:
        return render(request,'userinterfacefiles/productinformation.html')

def productinformation(request):
    items = ItemModel.objects.all()
    context={'items':items}
    
    return render(request,'userinterfacefiles/productinformation.html',context)

def orderproduct1(request):
    item_id = request.POST['item_id']
    item_adding = ItemModel.objects.get(itemid=request.POST['item_id'])
    item_quantity = request.POST['item_quantity']
    #orderModel = OrderModel.objects.create(user=request.user)
    orderItemModel = OrderItemModel.objects.create(
        item =item_adding,
        ordered=False,
        quantity=item_quantity
    )
    orderItemModel.save()

    return render(request,'userinterfacefiles/orderproduct.html')

def orderproduct(request):
    if request.user.is_authenticated:
        userModel = UserProfileRegistrationModel.objects.get(email=request.user.email)
        orderModel, is_order_placed = OrderModel.objects.get_or_create(user=userModel,ordered=False)
        item_id = request.GET.get("item_id")
        print(item_id)
        item_adding = ItemModel.objects.get(itemid=item_id)
        # item_quantity = request.POST['item_quantity']
        item_quantity = 1
        
        # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
        if OrderItemModel.objects.filter(order=orderModel,item=item_adding,user=userModel).exists():
            order_entry_exist = OrderItemModel.objects.get(order=orderModel,item=item_adding,user=userModel)
            qty_already_added = order_entry_exist.quantity
            new_qty = int(item_quantity)
            old_and_new_qty = qty_already_added+new_qty
            order_entry_exist.quantity=old_and_new_qty
            user=userModel
            order_entry_exist.orderId = orderModel.id
            
            order_entry_exist.save()
            # orderModel.items.add(order_entry_exist)
        else:
            orderItemModel = OrderItemModel.objects.create(
            user=userModel,
            item =item_adding,
            ordered=True,
            order =orderModel,
            orderId = orderModel.id,
            quantity=item_quantity
            ).save()
            # orderModel.items.add(orderItemModel)
        items = ItemModel.objects.all()
        context={'items':items}
        return render(request,'userinterfacefiles/productinformation.html',context)
    else:
        orderModel, is_order_placed = OrderModel.objects.get_or_create(ordered=False)
        item_id = request.GET.get("item_id")
        print(item_id)
        item_adding = ItemModel.objects.get(itemid=item_id)
        # item_quantity = request.POST['item_quantity']
        item_quantity = 1
        orderItemModel = OrderItemModel.objects.create(
            item =item_adding,
            ordered=True,
            order =orderModel,
            orderId = orderModel.id,
            quantity=item_quantity
            ).save()
            # orderModel.items.add(orderItemModel)
        items = ItemModel.objects.all()
        context={'items':items}
        return render(request,'userinterfacefiles/productinformation.html',context)

def shoppyLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            userModel = UserProfileRegistrationModel.objects.get(email=email)
        except ObjectDoesNotExist:
            context={
                'authenticated':'Authentication failed, Please provide correct details',
                'email':email
            }
            return render(request,'userinterfacefiles/shoppylogin.html',context)

        
        chkpwd = check_password(password, userModel.password)

        if chkpwd:
            print(userModel.username)
            user = authenticate(username = userModel.username, password=password)
            login(request,user)
            subject = 'We are from Shoppy, Login Notification'
            message = 'Hello '+userModel.first_name+'\n\n\nWe are letting you that, someone just login into your account.\n\nPlease check it, if it is not you.\n\n\n\nRegards\n\nShoppy Admin Team'
            
            email_from =settings.EMAIL_HOST_USER
            recipient_list = [userModel.email ]
            send_mail( subject, message, email_from, recipient_list )
            context={
                'authenticated':'you are authenticated'
            }
            return redirect(productinformation)
        else:
            context={
                'authenticated':'Authentication failed, Please provide correct details',
                'email':email
            }
            return render(request,'userinterfacefiles/shoppylogin.html',context)

    return render(request,'userinterfacefiles/shoppylogin.html')

def logout_view(request):

    logout(request)
    return render(request,'userinterfacefiles/shoppylogin.html')

def cart(request):
    if request.user.is_authenticated:
        userModel = UserProfileRegistrationModel.objects.get(email=request.user.email)  
        orderModel, is_order_placed = OrderModel.objects.get_or_create(user=userModel,ordered=False)
        # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
        all_added_items = orderModel.orderitemmodel_set.all()
    
        total_bucket_price=0
        total_bucket_quantity=0
        for item in all_added_items:
            total_bucket_price += item.get_total_item_price()
            total_bucket_quantity +=item.quantity
        
        context={
            'all_added_items':all_added_items,
            'total_bucket_price':round(total_bucket_price,2),
            'total_prodcuts_added':len(all_added_items),
            'total_bucket_quantity':total_bucket_quantity
        }
        
        return render(request,'userinterfacefiles/bucket.html',context)
    else:
        orderModel, is_order_placed = OrderModel.objects.get_or_create(ordered=False)
        # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
        all_added_items = orderModel.orderitemmodel_set.all()

        total_bucket_price=0
        total_bucket_quantity=0
        for item in all_added_items:
            total_bucket_price += item.get_total_item_price()
            total_bucket_quantity +=item.quantity
        
        context={
            'all_added_items':all_added_items,
            'total_bucket_price':round(total_bucket_price,2),
            'total_prodcuts_added':len(all_added_items),
            'total_bucket_quantity':total_bucket_quantity
        }
        
        return render(request,'userinterfacefiles/bucket.html',context)

def do_not_need_this_item(request):

    userModel = UserProfileRegistrationModel.objects.get(email=request.user.email)  
    orderModel, is_order_placed = OrderModel.objects.get_or_create(user=userModel,ordered=False)
    # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
    item_id = request.GET.get("item_id")
    removeItemModel = OrderItemModel.objects.get(id=item_id)
    print(removeItemModel.id)
    removeItemModel.delete()
    # orderModel.items.remove(removeItemModel)
    orderModel_new, is_order_placed = OrderModel.objects.get_or_create(user=userModel,ordered=False)
    all_added_items = OrderItemModel.objects.filter(orderId = orderModel.id)
    # print(orderModel.get_total_bucket_price())
    total_bucket_price=0
    total_bucket_quantity=0
    for item in all_added_items:
        print(item.id)
        # print(item.item.imageUrl)
        # print(item.get_total_item_price())
        total_bucket_price += item.get_total_item_price()
        total_bucket_quantity +=item.quantity

    
    # print(total_bucket_price)

    context={
        'all_added_items':all_added_items,
        'total_bucket_price':round(total_bucket_price,2),
        'total_prodcuts_added':len(all_added_items),
        'total_bucket_quantity':total_bucket_quantity
    }

    return render(request,'userinterfacefiles/bucket.html',context)

def update_quantity(request):
    print("this is from update_quantity")
    userModel = UserProfileRegistrationModel.objects.get(email=request.user.email)  
    orderModel, is_order_placed = OrderModel.objects.get_or_create(user=userModel,ordered=False)
    item_id = request.POST.get('item_id')
    quantity = request.POST.get('quantityselected')
    # print(item_id)
    # print(quantity)
    itemModel = OrderItemModel.objects.get(id=item_id)
    # print(itemModel.quantity)
    itemModel.quantity = quantity
    itemModel.orderId = orderModel.id
    itemModel.save()
    orderModel.save()
    
    # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
    all_added_items = orderModel.orderitemmodel_set.all()
    # all_added_items = OrderItemModel.objects.filter(orderId=orderModel.id)
    total_bucket_price=0
    total_bucket_quantity=0
    for item in all_added_items:
        total_bucket_price += item.get_total_item_price()
        total_bucket_quantity +=item.quantity

    context={
        'all_added_items':all_added_items,
        'total_bucket_price':round(total_bucket_price,2),
        'total_prodcuts_added':len(all_added_items),
        'total_bucket_quantity':total_bucket_quantity
    }
    
    return render(request,'userinterfacefiles/bucket.html',context)

def proceedtocheckout(request):
    userModel = UserProfileRegistrationModel.objects.get(email=request.user.email)  
    orderModel, is_order_placed = OrderModel.objects.get_or_create(user=userModel,ordered=False)
    shippingAddresses = ShippingAdress.objects.filter(user=userModel)
    # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
    all_added_items = orderModel.orderitemmodel_set.all()
    # all_added_items = OrderItemModel.objects.filter(orderId=orderModel.id)
    # print(orderModel.get_total_bucket_price())
    total_bucket_price=0
    total_bucket_quantity=0
    for item in all_added_items:
        # print(item.id)
        # print(item.item.imageUrl)
        # print(item.get_total_item_price())
        total_bucket_price += item.get_total_item_price()
        total_bucket_quantity +=item.quantity

    
    # print(total_bucket_price)

    context={
        'all_added_items':all_added_items,
        'total_bucket_price':round(total_bucket_price,2),
        'total_prodcuts_added':len(all_added_items),
        'total_bucket_quantity':total_bucket_quantity,
        'shippingAddresses':shippingAddresses,
        'bucketId':orderModel.id
    }
    
    return render(request,'userinterfacefiles/checkout.html',context)

def continue_to_checkout(request):
    userModel = UserProfileRegistrationModel.objects.get(email=request.user.email)
    orderModel, is_order_placed = OrderModel.objects.get_or_create(user=userModel,ordered=False)
    billingAddressModel,orderPlaced = BillingAddressModel.objects.get_or_create(orderId=orderModel.id,orderPlaced=False)
    # shippingAddress,orderPlaced = ShippingAdress.objects.get_or_create(orderId=orderModel.id,orderPlaced=False)
    paymentModel,orderPlaced = PaymentModel.objects.get_or_create(orderId=orderModel.id,orderPlaced=False)
    all_added_items = orderModel.orderitemmodel_set.all()
    # all_added_items = OrderItemModel.objects.filter(orderId=orderModel.id)
    total_bucket_price=0
    total_bucket_quantity=0
    for item in all_added_items:
        total_bucket_price += item.get_total_item_price()
        total_bucket_quantity +=item.quantity
    
    
    oldAddress = int(request.POST.get('oldAddress'))
    print(oldAddress)
    if oldAddress != 0:
        print("the value is NOT zero")
        shippingAddress = ShippingAdress.objects.get(id=oldAddress)
        orderModel.shippingAddress = shippingAddress
        orderModel.save()
    else: 
        print("the value is zero")
        fullname = request.POST.get('shippingAddress_fullname')
        email    = request.POST.get('shippingAddress_email')
        address  = request.POST.get('shippingAddress_address')
        city     = request.POST.get('shippingAddress_city')
        state    = request.POST.get('shippingAddress_state')
        zipcode  = request.POST.get('shippingAddress_zipcode')
        shippingAddress = ShippingAdress.objects.create(
        fullName=fullname,
        email=email,
        completeStreetAddress=address,
        city=city,
        state=state,
        zipcode=zipcode,
        # orderId=orderModel.id,
        user = userModel)
        shippingAddress.save()
        orderModel.shippingAddress = shippingAddress
        orderModel.save()

    billing_shipping_not_same = request.POST.get('billing_shipping_not_same')
    if billing_shipping_not_same :
        fullname = request.POST.get('billingAddress_fullname')
        email    = request.POST.get('billingAddress_email')
        address  = request.POST.get('billingAddress_address')
        city     = request.POST.get('billingAddress_city')
        state    = request.POST.get('billingAddress_state')
        zipcode  = request.POST.get('billingAddress_zipcode')
        billingAddressModel.fullName=fullname
        billingAddressModel.email=email
        billingAddressModel.address=address
        billingAddressModel.city=city
        billingAddressModel.state=state
        billingAddressModel.zipcode=zipcode
        billingAddressModel.orderId=orderModel.id
        billingAddressModel.user = userModel
        billingAddressModel.save()
    else:
        shippingAddress = orderModel.shippingAddress
        billingAddressModel.fullName=shippingAddress.fullName
        billingAddressModel.email=shippingAddress.email
        billingAddressModel.address=shippingAddress.completeStreetAddress
        billingAddressModel.city=shippingAddress.city
        billingAddressModel.state=shippingAddress.state
        billingAddressModel.zipcode=shippingAddress.zipcode
        billingAddressModel.orderId=orderModel.id
        billingAddressModel.user = userModel
        billingAddressModel.save()
        
    
    orderModel.billingAddress = billingAddressModel
    orderModel.save()
    # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
    
    context={
        'all_added_items':all_added_items,
        'total_bucket_price':round(total_bucket_price,2),
        'total_prodcuts_added':len(all_added_items),
        'total_bucket_quantity':total_bucket_quantity,
        'shippingAddress':orderModel.shippingAddress,
        # 'paymentModel':paymentModel
    }
    return render(request,'userinterfacefiles/orderreview.html',context)

def continue_to_payment(request):
    userModel = UserProfileRegistrationModel.objects.get(email=request.user.email)
    orderModel, is_order_placed = OrderModel.objects.get_or_create(user=userModel,ordered=False)
    billingAddressModel,orderPlaced = BillingAddressModel.objects.get_or_create(orderId=orderModel.id,orderPlaced=False)
    # shippingAddress,orderPlaced = ShippingAdress.objects.get_or_create(orderId=orderModel.id,orderPlaced=False)
    paymentModel,orderPlaced = PaymentModel.objects.get_or_create(orderId=orderModel.id,orderPlaced=False)
    all_added_items = orderModel.orderitemmodel_set.all()
    # all_added_items = OrderItemModel.objects.filter(orderId=orderModel.id)
    total_bucket_price=0
    total_bucket_quantity=0
    for item in all_added_items:
        total_bucket_price += item.get_total_item_price()
        total_bucket_quantity +=item.quantity
    
    
    oldAddress = int(request.POST.get('oldAddress'))
    print(oldAddress)
    if oldAddress != 0:
        print("the value is NOT zero")
        shippingAddress = ShippingAdress.objects.get(id=oldAddress)
        orderModel.shippingAddress = shippingAddress
        orderModel.save()
    else: 
        print("the value is zero")
        fullname = request.POST.get('shippingAddress_fullname')
        email    = request.POST.get('shippingAddress_email')
        address  = request.POST.get('shippingAddress_address')
        city     = request.POST.get('shippingAddress_city')
        state    = request.POST.get('shippingAddress_state')
        zipcode  = request.POST.get('shippingAddress_zipcode')
        shippingAddress = ShippingAdress.objects.create(
        fullName=fullname,
        email=email,
        completeStreetAddress=address,
        city=city,
        state=state,
        zipcode=zipcode,
        # orderId=orderModel.id,
        user = userModel)
        shippingAddress.save()
        orderModel.shippingAddress = shippingAddress
        orderModel.save()

    billing_shipping_not_same = request.POST.get('billing_shipping_not_same')
    if billing_shipping_not_same :
        fullname = request.POST.get('billingAddress_fullname')
        email    = request.POST.get('billingAddress_email')
        address  = request.POST.get('billingAddress_address')
        city     = request.POST.get('billingAddress_city')
        state    = request.POST.get('billingAddress_state')
        zipcode  = request.POST.get('billingAddress_zipcode')
        billingAddressModel.fullName=fullname
        billingAddressModel.email=email
        billingAddressModel.address=address
        billingAddressModel.city=city
        billingAddressModel.state=state
        billingAddressModel.zipcode=zipcode
        billingAddressModel.orderId=orderModel.id
        billingAddressModel.user = userModel
        billingAddressModel.save()
    else:
        shippingAddress = orderModel.shippingAddress
        billingAddressModel.fullName=shippingAddress.fullName
        billingAddressModel.email=shippingAddress.email
        billingAddressModel.address=shippingAddress.completeStreetAddress
        billingAddressModel.city=shippingAddress.city
        billingAddressModel.state=shippingAddress.state
        billingAddressModel.zipcode=shippingAddress.zipcode
        billingAddressModel.orderId=orderModel.id
        billingAddressModel.user = userModel
        billingAddressModel.save()
        
    # cardname    = request.POST.get('cardname')
    # cardnumber  = request.POST.get('cardnumber')
    # expmonth    = request.POST.get('expmonth')
    # expyear     = request.POST.get('expyear')
    # cvv         = request.POST.get('cvv')
    
    
    # paymentModel.methodUsed='card'
    # paymentModel.amount     = total_bucket_price
    # paymentModel.user = userModel
    # paymentModel.amount = total_bucket_price
    # paymentModel.nameOnCard=cardname
    # paymentModel.cardNumber=cardnumber
    # paymentModel.ExpMonth=expmonth
    # paymentModel.ExpYear=expyear
    # paymentModel.cvv=cvv
    # paymentModel.orderId=orderModel.id
    # paymentModel.save()

    # orderModel.shippingAddress = shippingAddress
    orderModel.billingAddress = billingAddressModel
    orderModel.save()
    # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
    
    context={
        'all_added_items':all_added_items,
        'total_bucket_price':round(total_bucket_price,2),
        'total_prodcuts_added':len(all_added_items),
        'total_bucket_quantity':total_bucket_quantity,
        'shippingAddress':orderModel.shippingAddress,
        # 'paymentModel':paymentModel
    }
    return render(request,'userinterfacefiles/continue_payment.html',context)

from datetime import datetime
def order_confirmation_page(request):

    userModel = UserProfileRegistrationModel.objects.get(email=request.user.email)  
    orderModel, is_order_placed = OrderModel.objects.get_or_create(user=userModel,ordered=False)
    billingAddressModel,orderPlaced = BillingAddressModel.objects.get_or_create(orderId=orderModel.id,orderPlaced=False)
    billingAddressModel.orderPlaced = True
    billingAddressModel.save()

    all_added_items = orderModel.orderitemmodel_set.all()
    # all_added_items = OrderItemModel.objects.filter(orderId=orderModel.id)
    total_bucket_price=0
    total_bucket_quantity=0
    for item in all_added_items:
        total_bucket_price += item.get_total_item_price()
        total_bucket_quantity +=item.quantity
    
    payment_method = request.POST.get('payment')
    paymentModel,orderPlaced = PaymentModel.objects.get_or_create(orderId=orderModel.id,orderPlaced=False)
    paymentModel.orderId = orderModel.id
    if payment_method == 'card':
        cardname    = request.POST.get('cardname')
        cardnumber  = request.POST.get('cardnumber')
        expmonth    = request.POST.get('expmonth')
        expyear     = request.POST.get('expyear')
        cvv         = request.POST.get('cvv')
        paymentModel.methodUsed='card'
        paymentModel.amount = total_bucket_price
        paymentModel.user = userModel
        paymentModel.nameOnCard = cardname
        paymentModel.cardNumber = cardnumber
        paymentModel.ExpMonth = expmonth
        paymentModel.ExpYear = expyear
        paymentModel.cvv = cvv
        paymentModel.orderPlaced = True
        paymentModel.save()
    else:
        paymentModel.methodUsed ='paypal'
        paymentModel.amount = total_bucket_price
        paymentModel.user = userModel
        # paymentModel.nameOnCard = ''
        # paymentModel.cardNumber = ''
        # paymentModel.ExpMonth = ''
        # paymentModel.ExpYear = ''
        # paymentModel.cvv = ''
        paymentModel.orderPlaced = True
        paymentModel.save()


    orderModel.ordered=True
    orderModel.ordered_date = datetime.now()
    orderModel.payment= paymentModel
    orderModel.save()

    all_added_items = orderModel.orderitemmodel_set.all()
    # all_added_items = OrderItemModel.objects.filter(orderId = orderModel.id)
    total_bucket_price=0
    total_bucket_quantity=0
    for item in all_added_items:
        total_bucket_price += item.get_total_item_price()
        total_bucket_quantity +=item.quantity
    
    context={
        'all_added_items':all_added_items,
        'total_bucket_price':round(total_bucket_price,2),
        'total_prodcuts_added':len(all_added_items),
        'total_bucket_quantity':total_bucket_quantity,
        'billingAddress':billingAddressModel,
        'paymentModel':paymentModel
    }
    template = render_to_string('userinterfacefiles/order_confirmation_email.html',context)
    subject_line = 'Shoppy - Order Confirmation Email for:'+str(orderModel.id)
    simple_message = strip_tags(template)
    to_user = [request.user.email] 
    from_shoppy_admin = settings.EMAIL_HOST_USER
    mail.send_mail(subject_line, simple_message, from_shoppy_admin, to_user, html_message=template)
    
    return render(request,'userinterfacefiles/order_confirmationpage.html',context)

def previous_orders(request):
    
    userModel = UserProfileRegistrationModel.objects.get(email=request.user.email) 
    previous_orders = OrderModel.objects.filter(user=userModel,ordered=True)
    
    context={
        'previous_orders':previous_orders
    }
    return render(request,'userinterfacefiles/previous_orders.html',context)

import json
from django.http import HttpResponse,JsonResponse

def completePayment(request):
    body = json.loads(request.body)
    cartId = body.get('cartId')
    # paymentTypeUsed = body.get('paymentType')
    orderModel = OrderModel.objects.get(id=cartId)
    # cartEntries = cart.cartentry_set.all()
    # deliveryAddress = cart.address
    # orderModel.ordered=True
    # cart.status="Processing"
    # cart.paymentTypeUsed=paymentTypeUsed
    orderModel.save()
    # sendOrderConfirmationEmail(cart)
    return JsonResponse("<h1><br><br>Payment processed successfully</h1>",safe=False)
    # return render(request, "htmlfiles/orderconfirmtionpage.html")
def account_settings(request):

    user = UserProfileRegistrationModel.objects.get(username=request.user.username)
    # user=request.user.username
    addresses= ShippingAdress.objects.filter(user=user)
    context ={
        'addresses':addresses
    }
    return render(request,'userinterfacefiles/account_settings.html',context)

def editaddress(request):
    addressId = request.GET.get("addressId")
    addresstoEdit = ShippingAdress.objects.get(id=addressId)
    fullName = request.POST['fullName']
    email = request.POST['email']
    completeStreetAddress = request.POST["completeStreetAddress"]
    city = request.POST["city"]
    state = request.POST["state"]
    zipcode = request.POST["zipcode"]
    addresstoEdit.fullName=fullName
    addresstoEdit.email=email
    addresstoEdit.completeStreetAddress=completeStreetAddress
    addresstoEdit.city=city
    addresstoEdit.state=state
    addresstoEdit.zipcode=zipcode
    addresstoEdit.save()
    context={}
    user = UserProfileRegistrationModel.objects.get(username=request.user.username)
    # user=request.user.username
    addresses= ShippingAdress.objects.filter(user=user)
    context ={
        'addresses':addresses,
        'editmessage':'The address has been saved'
    }
    return render(request,'userinterfacefiles/account_settings.html',context)

def deleteaddress(request):
    addressId = request.GET.get("addressId")
    addresstoDelete = ShippingAdress.objects.get(id=addressId)
    addresstoDelete.delete()
    context={}
    context={}
    user = UserProfileRegistrationModel.objects.get(username=request.user.username)
    addresses= ShippingAdress.objects.filter(user=user)
    context ={
        'deletemessage':'The address has been deleted from the list',
        'addresses':addresses
    }
    return render(request,'userinterfacefiles/account_settings.html',context)

def addnewaddress(request):
    if request.method == 'POST':
        newAddreess = ShippingAdress.objects.create()
        fullName = request.POST['fullName']
        email = request.POST['email']
        completeStreetAddress = request.POST["completeStreetAddress"]
        city = request.POST["city"]
        state = request.POST["state"]
        zipcode = request.POST["zipcode"]

        user = UserProfileRegistrationModel.objects.get(username=request.user.username)

        shippingAddress = ShippingAdress.objects.create(
        fullName=fullName,
        email=email,
        completeStreetAddress=completeStreetAddress,
        city=city,
        state=state,
        zipcode=zipcode,
        user = user)
        shippingAddress.save()
        
        addresses= ShippingAdress.objects.filter(user=user)
        
        context ={
            'addmessage':'The address has been added to the list',
            'addresses':addresses
        }

        return render(request,'userinterfacefiles/account_settings.html',context)
    return render(request,'userinterfacefiles/account_settings.html')