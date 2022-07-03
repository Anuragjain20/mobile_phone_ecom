from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Color,Company,Rating,Mobile,Category,Images,CartItems,CartModel])