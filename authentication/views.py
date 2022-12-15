from . import email_logins
import smtplib
import threading
from threading import Thread
from django.views.generic import View
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
#fro activate user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
# getting token from utils
from .utils import generate_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# for emailfro 
from django.core.mail import send_mail,EmailMultiAlternatives, BadHeaderError
# from django.core.mail import EmailMessage
from email.message import EmailMessage
from django.core import mail
from django.conf import settings

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)
    def run(self):
        self.email_message.send()


# Create your views here.
def signup(request):
    print("comming")
    if request.method=="POST":
        email = request.POST["email"]
        password = request.POST["pass1"]
        confirm_password = request.POST["pass2"]
        if password != confirm_password:
            print("Not Match")
            messages.warning(request,"Password is not Matching")
            return render(request,"auth/signup.html")
        try:    
            if User.objects.get(username=email):
                print("matcing......")
                messages.warning(request,"email already taken")
                return render(request,"auth/signup.html")
        except Exception as identifier:
            # pass
            user = User.objects.create_user(email,email,password)
            user.is_active=False
            user.save() 
            current_site = get_current_site(request)
            message=render_to_string("auth/activate.html",{
                "user":user,
                 "domain":current_site,
                 "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                 "token":generate_token.make_token(user),
                  
            })
            msg = EmailMessage()
            msg.set_content(message)
            msg['Subject'] = "Activate you store account"
            msg['From'] = "info@ssebowa.com"
            msg['To'] = email
            s = smtplib.SMTP_SSL(email_logins.SERVER, email_logins.PORT)
            s.login(email_logins.EMAIL,email_logins.PASS)
            # Sending the message
            s.send_message(msg)
            s.quit()
            # email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            # EmailThread(email_message).start()
            messages.info(request,"Activate your account by clicking the link in your Mail Box")
            return redirect("/auth/login") 
    return render(request,'auth/signup.html')

class ActivateAccount(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active= True
            user.save()
            messages.info(request,"Account activated successfully")
            return redirect('/auth/login/')
        return render('auth/activate_fail.html')


def handlelogin(request):
    if request.method=="POST":

        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            print("comming    1111")
            login(request,myuser)
            print("comming")

            messages.success(request,"Login Success")
            return render(request,'index.html')

        else:
            messages.error(request,"Something went wrong")
            return redirect("/auth/login/")

    return render(request,"auth/login.html")

def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('/auth/login/')

class RequestEmailReset(View):
    def get(self,request):
        return render(request,"auth/request-email.html")

    def post(self,request):
        email = request.POST['email']
        user=User.objects.filter(email=email)
        print(user)
        # try:
        if user.exists:
            current_site = get_current_site(request)
            email_subject = "Reset your account"
            print("commin...")
            message=render_to_string("auth/reset-user-password.html",{
                "user":user,
                "domain":'127.0.0.1:8000',
                "uid":urlsafe_base64_encode(force_bytes(user[0].pk)),
                "token":PasswordResetTokenGenerator().make_token(user[0]),
                
            })
            print(message)
            email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            print("******************")
            # EmailThread(email_message).start()
            messages.info(request,"Activate your account by clicking the link in your Mail Box")
            EmailThread(email_message).start()
            messages.info(request,"we have send the email of a link to reset your password")
            return render(request,"auth/request-email.html")
        # except:
        #     messages.info(request,"something went wrong")
        #     return render(request,"auth/request-email.html")
            
class SetNewPassword(View):
    def get(self,request,uidb64,token):
        context={
            "uidb64":uidb64,
            "token":token,
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"password reset link is invalid")
                return render(request,"auth/request-email.html")
            
        except DjangoUnicodeDecodeError as indentifier:
            pass
        
        return render(request,"auth/set-new-password.html",context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token,
        }
        password = request.POST["pass1"]
        confirm_password = request.POST["pass2"]
        if password != confirm_password:
            print("Not Match")
            messages.warning(request,"Password is not Matching")
            return render(request,"auth/set-new-password.html")
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            print("coming..")
            messages.success(request,"password reset success please login with new password")
            return redirect('/auth/login/')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something went wrong")
            return render(request,'auth/set-new-password.html',context)

        # return render(request,'auth/set-new-password.html')