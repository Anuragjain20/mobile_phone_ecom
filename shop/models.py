from django.db.models.signals import pre_save, post_save,post_delete
from django.dispatch import receiver
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from authen.models import Profile
from PIL import Image
# Create your models here.
class Color(models.Model):
    name = models.CharField(max_length=50)
    hex = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='company_logos')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)



    
    def save(self, *args, **kwargs):
        if not self.owner.is_client:
            super().save(*args, **kwargs)
            img = Image.open(self.logo.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.logo.path) 
        else:
            raise ValueError('You are not a owner')

           
    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name    

          

class Mobile(models.Model):
    title= models.CharField(max_length=50)
    price = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE,related_name='mobiles')
    features = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='mobiles')
    quatity = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="mobiles")
    



    def __str__(self):
        return self.title        



class Images(models.Model):
    image = models.ImageField(upload_to='mobile_images')
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name='images')

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return str(self.mobile)                

class Rating(models.Model):
    rating = models.IntegerField(default=0,validators=[MaxValueValidator(5),MinValueValidator(0)])
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ratings')
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return str(self.rating)          

    # check whether user is client before save

    def save(self, *args, **kwargs):
        if not self.user.is_client:
            raise ValueError('You are not a client')
        else:
            super().save(*args, **kwargs)    

class CartModel(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cart')
    is_paid = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    total_amt = models.FloatField(default=0)
    razor_pay_order_id = models.CharField(max_length=1000 , null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=100 , null=True , blank=True)
    razorpay_signature = models.CharField(max_length=100 , null=True , blank=True)

class CartItems(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cart_items')
    cart = models.ForeignKey(CartModel, related_name="cart_items", on_delete=models.CASCADE)
    item = models.ForeignKey(Mobile, related_name="cart_items", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.FloatField(default=0)


@receiver(pre_save, sender=CartItems)
def get_total_amt(sender, instance, *args, **kwargs):
    instance.total = instance.item.price * instance.quantity

@receiver(post_save, sender=CartItems)
def get_total_amt(sender, instance, *args, **kwargs):
    total=0
    cart_obj = CartModel.objects.get(owner = instance.owner, is_paid=False)
    for i in CartItems.objects.filter(cart=cart_obj):
        total += i.total
    cart_obj.total_amt = total
    cart_obj.save()

@receiver(post_delete,sender = CartItems)
def get_total_amt(sender,instance,*args,**kwargs):
    total = 0
    cart_obj = CartModel.objects.get(owner = instance.owner, is_paid=False)
    for i in CartItems.objects.filter(cart=cart_obj):
        total += i.total
    cart_obj.total_amt = total
    cart_obj.save()

