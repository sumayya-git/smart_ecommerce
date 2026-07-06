from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings



User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")
    slug = models.SlugField(unique=True,blank=True)
    image = models.ImageField(upload_to='categories/', null= True, blank=True)

    

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(default=4)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s cart"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name}({self.quantity})"
    

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100,blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, blank=True)
   

    def __str__(self):
        return self.user.username

  
class Order(models.Model):
    
    STATUS_CHOICES = (
        ('PLACED','Placed'),
        ('PROCESSING', 'Processing'),
        ('PACKED','Packed'),
        ('SHIPPED', 'Shipped'),
        ('CANCEL_REQUESTED', 'Cancel Requested'),
        ('CANCELLED','Cancelled'),
        ('DELIVERED', 'Delivered'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20, choices= STATUS_CHOICES, default="PLACED")
   
    

    

    REFUND_STATUS_CHOICES = (
    #models.CharField(max_length=20, choices=[
        ("NOT_INITIATED", "Not Initiated"),
        ("INITIATED", "Initiated"),
        ("COMPLETED", "Completed"),
    #],
    # default="NOT_INITIATED"
    )

    # refund_status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default="NOT_INITIATED")

    PAYMENT_STATUS_CHOICES = (
        #models.CharField(max_length=20,choices=[
                                          ("PENDING","Pending"),
                                          ("PAID", "Paid"),
                                     # ],
                                     # default="PENDING"
                                      )
    
    
   
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING"

    )

    PAYMENT_METHOD_CHOICES =(
        
        ("ONLINE", "Online"),
        ("COD","Cash On Delivery"),
    )

    payment_method = models.CharField( max_length=20, choices=PAYMENT_METHOD_CHOICES, default="ONLINE")

    RETURN_STATUS = (
        ("NONE", "None"),
        ("REQUESTED","Requested"),
        ("APPROVED","Approved"),
        ("REJECTED","Rejected"),
    )

    return_status = models.CharField(max_length=20, choices=RETURN_STATUS, default="NONE")

    refund_status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default="NOT_INITIATED")

    cancel_reason = models.TextField(blank=True, null=True)

    cancelled_at = models.DateTimeField(blank=True, null=True)


    
    placed_at = models.DateTimeField(default=timezone.now)
    packed_at = models.DateTimeField(null=True,blank=True)
    shipped_at = models.DateTimeField(null=True,blank=True)
    delivered_at = models.DateTimeField(null=True,blank=True)
        
    
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank = True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    invoice_sent = models.BooleanField(default=False)

        # Refund Details (For COD Orders)
    refund_account_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    refund_account_number = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    refund_ifsc = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    refund_upi_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
        

    def __str__(self):
        return f"Order #{self.id}"
    
   
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name="items",on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cancelled_qty = models.PositiveIntegerField(default=0)

    def effective_qty(self):
        return self.quantity - self.cancelled_qty
    

       
    @property
    def subtotal(self):
        return self.price * self.effective_qty()
    
    def __str__(self):
        return self.product.name
    

   

