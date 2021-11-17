from django.db import models
from django.contrib.auth.models import User 


class ItemModel(models.Model):
    itemid = models.IntegerField(blank=False,unique=True)
    price = models.FloatField(max_length=10,blank=True)
    itemname = models.CharField(null=True,max_length=150,blank=True)
    description =models.TextField(max_length=1000,null=True,blank=True)
    category = models.CharField(max_length=10)
    label = models.CharField(max_length=10)
    #every item must have it own url
    imageUrl = models.TextField(blank=True,max_length=450)


class UserProfileRegistrationModel(User):
    #Below attributes are available in User inbuilt model
    # email
    # password
    # username
    # first_name
    # last_name

    mobilno = models.TextField()
    registered_on = models.DateTimeField(auto_now_add=True,auto_now=False)
    class Meta:
        Proxy:True
        
class BillingAddressModel(models.Model):
    fullName    = models.CharField(max_length=75,blank=False,null=True)
    email       = models.EmailField(max_length=50,blank=False,null=True)
    address     = models.CharField(max_length=50,blank=False,null=True)
    city        = models.CharField(max_length=50,blank=False,null=True)
    state       = models.CharField(max_length=50,blank=False,null=True)
    zipcode     = models.IntegerField(blank=False,null=True)
    orderId     = models.IntegerField(blank=True, null=True)
    orderPlaced = models.BooleanField(default=False,blank=True,null=True)
    user = models.ForeignKey(UserProfileRegistrationModel,on_delete=models.SET_NULL,blank=True,null=True)
    # country = models.CharField(max_length=50,blank=False)

class ShippingAdress(models.Model):
    fullName    = models.CharField(max_length=75,blank=False,null=True)
    email       = models.EmailField(max_length=50,blank=False,null=True)
    user       = models.ForeignKey(UserProfileRegistrationModel,on_delete=models.SET_NULL, blank=True, null=True)
    # address_type = models.CharField(max_length=15,blank=True, null=True)
    completeStreetAddress = models.CharField(max_length=200,blank=False,null=True)
    city = models.CharField(max_length=20,blank=False,null=True)
    state = models.CharField(max_length=20,blank=False,null=True)
    zipcode = models.IntegerField(blank=False,null=True)
    country = models.CharField(max_length=20,blank=False)
    orderId    = models.IntegerField(blank=True, null=True)
    orderPlaced = models.BooleanField(default=False,blank=True,null=True)

class OrderItemModel(models.Model):
    user = models.ForeignKey(UserProfileRegistrationModel,on_delete=models.SET_NULL,blank=True,null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # order = models.ForeignKey(OrderModel,on_delete=models.CASCADE)

    
    def get_total_item_price(self):
        return round(self.quantity * self.item.price,2)

    # def get_total_discount_item_price(self):
    #     return self.quantity * self.item.discount_price

    # def get_amount_saved(self):
    #     return self.get_total_item_price() - self.get_total_discount_item_price()

    # def get_final_price(self):
    #     if self.item.discount_price:
    #         return self.get_total_discount_item_price()
    #     return self.get_total_item_price()

class PaymentModel(models.Model):
    methodUsed = models.CharField(max_length=50,blank=True, null=True)
    user       = models.ForeignKey(UserProfileRegistrationModel,on_delete=models.SET_NULL, blank=True, null=True)
    amount     = models.FloatField(blank=True, null=True)
    nameOnCard = models.CharField(max_length=50,blank=True, null=True)
    cardNumber = models.CharField(max_length=20,blank=True, null=True)
    ExpMonth   = models.CharField(max_length=15,blank=True, null=True)
    ExpYear    = models.CharField(max_length=4,blank=True, null=True)
    cvv        = models.IntegerField(blank=True,null=True)
    orderId    = models.IntegerField(blank=True, null=True)
    orderPlaced= models.BooleanField(default=False,blank=True,null=True)


class OrderModel(models.Model):
    user = models.ForeignKey(UserProfileRegistrationModel,on_delete=models.SET_NULL,blank=True,null=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    # items = models.ManyToManyField(OrderItemModel)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True,null=True)
    ordered = models.BooleanField(default=False)
    shippingAddress = models.ForeignKey('ShippingAdress', related_name='shippingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    billingAddress = models.ForeignKey('BillingAddressModel', related_name='billingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('PaymentModel', on_delete=models.SET_NULL, blank=True, null=True)
    isDeliveryInProcess = models.BooleanField(default=False)
    isReceivedByCustomer = models.BooleanField(default=False)
    # order_total        = models.IntegerField(blank=True,null=True)

    def get_total_bucket_price(self):
        total_bucket_price=0
        for item in self.orderitemmodel_set.all():
            total_bucket_price += item.get_total_item_price()

        # print(round(total_bucket_price,2)) 
        return round(total_bucket_price,2)
    
    def total_quantity_of_all_items(self):
        total_bucket_quantity=0
        for item in self.orderitemmodel_set.all():
            total_bucket_quantity += item.quantity

        # print(total_bucket_quantity)
        return total_bucket_quantity

class OrderItemModel(models.Model):
    user = models.ForeignKey(UserProfileRegistrationModel,on_delete=models.SET_NULL,blank=True,null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    orderId = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey(OrderModel,on_delete=models.CASCADE,blank=True,null=True)
    

    def get_total_item_price(self):
        return round(self.quantity * self.item.price,2)