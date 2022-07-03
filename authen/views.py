
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login as auth_login
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.cache import cache
import random
from django.conf import settings
from .utils import send_forgot_link

class SignUpView(CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy("verify_otp")
    template_name = "signup.html"

def verify_otp(request):
    if request.method == 'POST':
        form = otpVerifyForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            email = cache.get(otp)
            if email:
                user = CustomUser.objects.get(email=email)
                user.is_verified = True
                user.save()
                cache.delete(otp)
                messages.success(request, "Your account has been verified successfully")
                return redirect('/accounts/login')
            else:
                messages.error(request, "Invalid OTP")
                return redirect('/accounts/verify_otp/')
 
    else:
        form = otpVerifyForm()
    return render(request, 'otpVerification.html', {'form': form})


    
def login(request):
  
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_verified:
                    auth_login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, "Please verify your account")
                    
                    return redirect('/accounts/verify_otp/')
            else:
                message = "Invalid Credentials"
                form = LoginForm()
                return render(request, 'login.html', {'form': form, 'error': message})


    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/accounts/login/')

def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required(login_url='/accounts/login/')
def profile(request):
    prof = Profile.objects.filter(user=request.user)
    if not prof:
        prof = Profile(user = request.user)
    else:
        prof = prof[0]

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=prof)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=prof)
    return render(request, 'profile.html', {'form': form})
                


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email)
            if user:
                obj = send_forgot_link(email)
                obj.run()
                messages.success(request, "Please check your email to reset your password")
                return redirect('/accounts/login/')
            else:
                messages.error(request, "Invalid Email")
                return redirect('/accounts/forgot_password/')
    else:
        form = ForgotForm()
    return render(request, 'forgot_password.html', {'form': form})
     
def reset_password(request,id):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = cache.get(id)
            cache.delete(id)

            user = CustomUser.objects.get(email = email)
            user.set_password(password)
            user.save()
            messages.success(request, "Password has been reset successfully")
            return redirect('/accounts/login/')
        else:
            print(form.errors)
    else:
        form = ResetForm()
    return render(request, 'reset_password.html', {'form': form})

