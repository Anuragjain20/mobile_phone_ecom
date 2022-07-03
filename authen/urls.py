from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('profile/', profile, name='profile'),
    path('change_password/', forgot_password, name='change_password'),
    path('reset/<str:id>/', reset_password, name='reset_password'),
]

