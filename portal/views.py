from django.shortcuts import render, redirect
from .models import Parent
from django.db.utils import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
import smtplib




def register(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST['password']

        try: 
            parent = Parent.objects.create_user(username=email, password=password)
            parent.save()
            login(request, user=parent)
        except Exception as e:
            print(e)
            return render(request, "portal/register.html", {
                "message": "The email already exists"
            })
        
        return redirect("dashboard")
    elif request.method == "GET":
         return render(request, "portal/register.html")

    

def logout_view(request):
    logout(request)
    return redirect("login")


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        parent = authenticate(request, password=password, username=email)
        if parent is not None:
            login(request, user=parent)
            return redirect("dashboard")
        else:
            return render(request, "portal/login.html", {"message": "Invalid Email or Password"})
        

    else:
        return render(request, "portal/login.html")

def send_email(sender, reciever, content):
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.ehlo()
        connection.starttls()
        connection.ehlo()
        # connection.login(user=sender, password=tiag lrtm ltrx snee)
        try:
            connection.sendmail(from_addr=sender,
                                to_addrs=reciever,
                                msg=f"Subject:Quotation\n\n{content}")
            print("Sent")
        except UnicodeError:
            print("Not Sent")
def forgot(request):
    if request.method == "POST":
        email = request.POST["email"]
        parent = Parent.objects.filter(username=email).first()
        if parent:
            # Generate a token and send an email
            token = default_token_generator.make_token(parent)
            uidb64 = urlsafe_base64_encode(force_bytes(parent.id))
            reset_url = f'{settings.BASE_URL}/reset-password/{uidb64}/{token}/'
            print("Sending email", reset_url)
            # send_email("atongjonathangmail.com", parent.email,f"Subject:Reset Password\n\n{reset_url}")
            return redirect("recover")
    return render(request, "portal/forgot.html")

def recover(request):
    return render(request, "portal/recover.html")

@login_required
def dashboard(request):
    return render(request, template_name="portal/dashboard.html")


def test(request):
    return render(request, 'portal/test.html')