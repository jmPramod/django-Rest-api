from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CategoryModel(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(unique=True,blank=True)
    def __str__(self):
        return self.name
    

class ProductModel(models.Model): 
    category=models.ForeignKey(CategoryModel,related_name='products',on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    desciption=models.TextField(blank=True) 
    price=models.DecimalField(max_digits=10,decimal_places=2) 
    image=models.ImageField(upload_to='products/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True) 
    def __str__(self): 
        return self.name  
    
    
    
    
     
class UserProfileModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.TextField(blank=True)
    avatar=models.URLField(blank=True)
    
    def __str__(self):
        return self.user.username
    
    
class OrderModel(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)   
    
    def __str__(self):
     if self.user:
         return f"Order {self.id} by {self.user.username}"
     return f"Order {self.id} (Guest)"

class OrderItemModels(models.Model):
    order=models.ForeignKey(OrderModel,related_name='item',on_delete=models.CASCADE)
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    
    
    def __str__(self):
        return f"{self.quantity} X {self.product.name}"    
    


class CartModel(models.Model):
    users=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Cart {self.id} for {self.user}'
    @property
    def total(self):
        return sum (item.subTotal for item in self.item.all())    
        
        
class CartItemModels(models.Model):
    cart=models.ForeignKey(CartModel,related_name='items',on_delete=models.CASCADE)
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return f'{self.quantity} X {self.product.name}'
    @property
    def subtotal(self):
        return self.quantity * self.product.price
    
    
    
            
        