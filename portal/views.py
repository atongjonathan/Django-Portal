from django.shortcuts import render, redirect
from .models import Parent
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.http.request import HttpRequest
import smtplib
import requests



def real_db():
    response = requests.get(
        "https://raw.githubusercontent.com/atongjonathan/Django-Portal/master/portal/sample_data.json")
    DB = response.json()
    DB = get_avatars(DB)
    return DB

def get_avatars(DB: list):
    for child in DB:
         child["img"]=f"https://ui-avatars.com/api/name={child['name'].replace(' ','+')}?rounded=true&background=random"
    return DB


def register(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST["email"]
        children = [child for child in DB if child["f_email"]
                    == email or child["m_email"] == email]
        no_of_children = len(children)
        if no_of_children == 0:
            return render(request, "portal/register.html",
             {"message": "Email provided is not recognised by the school. Visit school to update!"})
        password = request.POST['password']

        try:
            parent = Parent.objects.create_user(
                username=email, password=password)
            parent.save()
            login(request, user=parent)
        except Exception as e:
            print(e)
            return render(request, "portal/register.html", {
                "message": "The email already exists"
            })

        return redirect("choose")
    elif request.method == "GET":
        return render(request, "portal/register.html")


@login_required
def choose(request: HttpRequest):
    children = [child for child in DB if child["f_email"] == str(
        request.user) or child["m_email"] == str(request.user)]
    no_of_children = len(children)
    if no_of_children == 0:
        logout(request)
        return render(request, "portal/login.html", {"message": "Your Email is not attached to any child. Visit school to update!"})
    else:
        return render(request, "portal/choose.html", {"title": "Choose Child","children": children})


@login_required
def dashboard(request: HttpRequest, id):
    for child in DB:
        if child["id"] == id and (child["f_email"] == str(request.user) or child["m_email"] == str(request.user)):
            data = child
            return render(request, template_name="portal/dashboard.html", context={"data": data, "id":data["id"]})
        else:
            pass
    return render(request, "portal/choose.html", {"title": "Dashboard","message": " Your email is not recognised by the school. Visit school to update!"})



# Dashboard Addons

def statement(request: HttpRequest, id):
    for child in DB:
        if child["id"] == id and (child["f_email"] == str(request.user) or child["m_email"] == str(request.user)):
            data = child
            return render(request, "portal/statement.html", {"title": "Fee Statement","id": id, "data":data})    

def statement_print(request: HttpRequest, id):
    for child in DB:
        if child["id"] == id and (child["f_email"] == str(request.user) or child["m_email"] == str(request.user)):
            data = child    
    return render(request, "portal/statement_print.html", {"title": "Fee Statement - PDF","id": id, "data":data})    

def invite(request: HttpRequest, id):
    for child in DB:
        if child["id"] == id and (child["f_email"] == str(request.user) or child["m_email"] == str(request.user)):
            data = child  
    if request.method == "POST":
        email = request.POST["email"]
        message = f"Subject: Invite to the Ark Junior School\n\n{request.user} Welcomes you to check out the Ark Junior Schools"
        try:
            send_email(settings.EMAIL_HOST, email, message)
            return render(request, "portal/invite.html", {"title": "Invite","id": id, "data": data, "message": True})
        except Exception as e:
            print(e)
    for child in DB:
        if child["id"] == id and (child["f_email"] == str(request.user) or child["m_email"] == str(request.user)):
            data = child
            return render(request, "portal/invite.html", {"title": "Invite","id": id, "data": data})


def structure(request: HttpRequest):
    return render(request, "portal/structure.html", {"title": "Fee Structure",})


def login_view(request: HttpRequest):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        parent = authenticate(request, password=password, username=email)
        if parent is not None:
            login(request, user=parent)
            return redirect("choose")
        else:
            return render(request, "portal/login.html", {"title": "Fee Statement","message": "Invalid Email or Password"})

    else:
        if (request.user.is_anonymous):
            return render(request, "portal/login.html")
        else:
            return redirect("choose")
            # return HttpResponse("Invalid Path")

def logout_view(request: HttpRequest):
    logout(request)
    return redirect("logged_out")





def forgot(request: HttpRequest):
    if request.method == "POST":
        email = request.POST["email"]
        parent = Parent.objects.filter(username=email).first()
        if parent:
            # Generate a token and send an email
            token = default_token_generator.make_token(parent)
            uidb64 = urlsafe_base64_encode(force_bytes(parent.id))
            reset_url = f'{settings.BASE_URL}/reset-password/{uidb64}/{token}/'
            send_email('portal@thearkjuniorschool.com', email,f"Subject:Reset Password\n\n{reset_url}")
            return redirect("recover")
    return render(request, "portal/forgot.html", {"title": "Forgot Password",})


def recover(request: HttpRequest):
    return render(request, "portal/recover.html", {"title": "Change Password",})






def test(request: HttpRequest):
    return render(request, 'portal/test.html')




def logged_out(request: HttpRequest):
    return render(request, "portal/logged_out.html", {"title": "Logged Out",})


def contact(request: HttpRequest):
    return render(request, "portal/contact.html", {"title": "Contact"})

def contact_us(request: HttpRequest):
    return render(request, "portal/contact_us.html", {"title": "Contact Us",})



# HTTP Error 400
def page_not_found(request, exception):
    return render(request, "portal/error_404.html")






def send_email(sender, reciever, content):

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(user="portal@thearkjuniorschool.com", password="ioqm iivv yatz mbep\n")
        try:
            connection.sendmail(from_addr=sender,
                                to_addrs=reciever,
                                msg=content)
            print(f"Email Sent to {reciever}")
        except UnicodeError:
            print("Not Sent")

global DB
DB = real_db()