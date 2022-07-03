
from django.shortcuts import render,redirect
from authen.views import login
from shop.models import *
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from authen.decorate import check_form_filled

client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))




# Create your views here.
def index(request):
    mobiles = Mobile.objects.all()[8:16]
    companies = Company.objects.all()
    
    return render(request, 'index.html', {'mobiles': mobiles, 'companies': companies})

def show_all_phones(request): 
    mobiles = Mobile.objects.all()
    paginator = Paginator(mobiles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'AllPhones.html', {'mobiles': page_obj})   

@login_required(login_url="/accounts/login/")
@check_form_filled
def product_details(request, id):
    mobile = Mobile.objects.get(id=id)
   

    images = Images.objects.filter(mobile=mobile)
    mobile_quantity = 0
    cart_obj = CartModel.objects.filter(owner=request.user.profile, is_paid=False)
    if cart_obj:
        cart_items = CartItems.objects.filter(cart=cart_obj[0], item=mobile)
        if cart_items:

            mobile_quantity = cart_items[0].quantity

    return render(request, 'Productdetails.html', {'mobile': mobile,  'images': images, 'mobile_quantity': mobile_quantity})   


@login_required(login_url='/accounts/login/')
@check_form_filled
def add_to_cart(request, id):
    try:
        customer = request.user.profile
        cart_obj,_ =  CartModel.objects.get_or_create(owner=customer,is_paid = False)
        mobile = Mobile.objects.get(id=id)

        if cart_obj.cart_items.filter(item = mobile,cart = cart_obj,).exists():
            cart_item_obj = CartItems.objects.get(
                cart = cart_obj,
                item = mobile)
            cart_item_obj.quantity += 1 


            cart_item_obj.save()
        else:
            print("here")
            CartItems.objects.create(
                owner = customer,
                cart = cart_obj,
                item = mobile )
        mobile.quatity -= 1
        mobile.save()        

    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  

@login_required(login_url='/accounts/login/')
@check_form_filled
def remove_from_cart(request,id):
    try:
        customer = request.user.profile
        cart_obj,_ =  CartModel.objects.get_or_create(owner=customer,is_paid = False)
        mobile = Mobile.objects.get(id=id)
        cart_item_obj = CartItems.objects.get(
            owner = customer,
            cart = cart_obj,
            item = mobile)
        if cart_item_obj.quantity > 1:
            cart_item_obj.quantity -= 1
            cart_item_obj.save()
        else:        
            cart_item_obj.delete()


    except Exception as e:
        print(e)
    mobile.quatity += 1
    mobile.save()        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login/')
@check_form_filled
def cart(request):
    customer = request.user.profile
    cart_obj,_ =  CartModel.objects.get_or_create(owner=customer,is_paid = False)
    if cart_obj.total_amt == 0:
        return redirect("/")
    cart_items = CartItems.objects.filter(cart=cart_obj)
    total_quantity = 0
    payment = client.order.create(
        {'amount' : cart_obj.total_amt * 100 , 'currency' : 'INR' , 'payment_capture' :1 }
    )
    cart_obj.razor_pay_order_id = payment['id']
    cart_obj.save()

    for item in cart_items:
        total_quantity += item.quantity
       
    
    return render(request, 'cart.html', {'cart_items': cart_items,'order_id':payment['id'] , 'key_id' : settings.KEY_ID, 'total_quantity': total_quantity, 'cart_obj': cart_obj})    

@login_required(login_url='/accounts/login/')
def payment_successfull(request):
    try:
        razor_pay_order_id = request.GET.get('razorpay_order_id')
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        razorpay_signature = request.GET.get('razorpay_signature')   
        cart_obj = CartModel.objects.get(razor_pay_order_id = razor_pay_order_id)
        cart_obj.is_paid = True
        cart_obj.razorpay_payment_id = razorpay_payment_id
        cart_obj.razorpay_signature = razorpay_signature
        cart_obj.save()

        return render(request, 'payment_successfull.html')
    except Exception as e:
        print(e)
    
    return render(request, 'payment_unsuccessfull.html')