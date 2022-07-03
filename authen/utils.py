from threading import Thread
from random import randint
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.conf import settings
import uuid

class SendOtpMail(Thread):
    def __init__(self, email):
        self.email = email
        Thread.__init__(self)

    def run(self):
        try:
  

            print("heree")
            otp = randint(100000, 999999)

            email_description = "Your OTP is " + str(otp) + "." + " Please do not share this OTP with anyone."
            email  = EmailMessage(subject='OTP', body=email_description, to=[self.email])
            # print(email.from_email)
            email.send()
         
            cache.set(otp, self.email, timeout=300)
        
        except Exception as e:
            print(e)
       

class send_forgot_link(Thread):
    def __init__(self, email):
        self.email = email
        Thread.__init__(self)
    def run(self):
        try:
            token = str(uuid.uuid4())
            cache.set(token, self.email, timeout=350)
            subject = "Link to change password"
            message = f"The link to change your account password http://127.0.0.1:8000/accounts/reset/{token}/ \nIts valid only for 5 mins."
    
            print("Email send started")
            email  = EmailMessage(subject=subject, body=message, to=[self.email])
            email.send()

            print("Email send finished")
        except Exception as e:
                print(e)       

       

      
        
