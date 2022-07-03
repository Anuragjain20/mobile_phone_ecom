
from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

class CustomUser(AbstractUser):
    username = None # Here
    email = models.EmailField('email address', unique=True) 
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email' # Here
    REQUIRED_FIELDS = []

    objects = CustomUserManager() # Here

    class Meta:
        verbose_name = "custom user"
        verbose_name_plural = "custom users"

class Profile(models.Model):
    name = models.CharField(max_length=100)  
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='profile')
    phone = models.CharField(max_length=15)      
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    image = models.ImageField(upload_to='profile_images')
    is_brand_owner = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    
    # modify image before save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size =  (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_cart_count(self):
        try:
            cart = self.cart.get(is_paid = False)
            return cart.cart_items.count()
        except Exception as e:
            return 0
        