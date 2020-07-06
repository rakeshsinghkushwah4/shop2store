from django.db import models
from accounts.models import MyProfile
from seller.models import Product

# Create your models here.
class Orders(models.Model):
    customer = models.ForeignKey(MyProfile,on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    seller_complete = models.BooleanField(default=False)
    cr_date = models.DateField(auto_now_add=True)
    transiction_id = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return str(self.transiction_id)
    
    @property
    def get_orderitem(self):
        return self.orderitem_set.all()    

    @property
    def shipping(self):
        # this is a variable
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])
        print('rakeshssssldjfkd',total)
        return total
    
    @property
    def get_cart_items(self):
        totalitems = self.orderitem_set.all()
        print('rakeshssssldjfkd',totalitems)
        total = sum([items.quantity for items in totalitems])
        return total

class OrderItem(models.Model):
    status = (('Panding','Panding'),('Delivered','Delivered'))
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=status,default='Panding')
    quantity = models.IntegerField(default=0)
    cr_date = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):    
        total = self.product.discount_price*self.quantity
        return total   

    @property
    def get_review(self):
        try:
            review = Review.objects.filter(customer = self.order.customer,product_name =self.product)
            return review     
        except:
            pass

class ShippingAddress(models.Model):
    customer = models.ForeignKey(MyProfile,on_delete=models.CASCADE)
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    state = models.CharField(max_length=1000)
    zipcode = models.CharField(max_length=1000)
    cr_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Review(models.Model):
    customer = models.ForeignKey(to=MyProfile,on_delete=models.CASCADE)
    product_name = models.ForeignKey(to=Product,on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return str(self.customer)

class Comment(models.Model):
    post = models.ForeignKey(Product, related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=200, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # manually deactivate inappropriate comments from admin site
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies',on_delete=models.CASCADE)

    class Meta:
        
        # sort comments in chronological order by default
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {}'.format(self.name)