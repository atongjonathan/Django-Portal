from django.shortcuts import render, redirect
from .models import Parent
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.http.request import HttpRequest
from portal.utils import *
from django.contrib.auth import update_session_auth_hash
from logging import basicConfig, getLogger, INFO, StreamHandler, FileHandler
from . mpesa import Mpesa
from .statement_data import get_statements
import json

basicConfig(format="%(asctime)s | PORTAL | %(levelname)s | %(module)s | %(lineno)s | %(message)s",
            level=INFO, handlers={StreamHandler(), FileHandler("logs.txt")}, datefmt="%b-%d %Y - %I:%M %p")

logger = getLogger(__name__)




def register(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST["email"]
        children = [child for child in DB if child["f_email"]
                    == email or child["m_email"] == email]
        no_of_children = len(children)
        if no_of_children == 0:
            logger.info(f"No Child Associated with {email}")
            return render(request, "portal/register.html",
                          {"message": "Email provided is not recognised by the school. Visit school to update!"})
        password = request.POST['password']
        try:
            parent = Parent.objects.create_user(
                username=email, password=password)
        except Exception as e:
            logger.info(f"User {email} seems to exist.Error:{e}")
            return render(request, "portal/register.html", {
                "message": "The email already exists"
            })
        parent.save()
        logger.info(f"Parent {parent.username} saved!")
        send_my_email(template="welcome",
                      subject="Welcome to the Ark Kunior Parents Portal", recipient=email)
        login(request, user=parent)
        logger.info(f"User {request.user} logged in")
        return redirect("choose")
    return render(request, "portal/register.html")


@login_required
def choose(request: HttpRequest):
    children = [child for child in DB if child["f_email"] == str(
        request.user) or child["m_email"] == str(request.user)]
    no_of_children = len(children)
    if no_of_children == 0:
        logger.error(
            f"Forced log out due to no child associate to {request.user}")
        logout(request)
        return render(request, "portal/login.html", {"message": "Your Email is not attached to any child. Visit school to update!"})
    return render(request, "portal/choose.html", {"title": "Choose Child", "children": children})


@login_required
def dashboard(request: HttpRequest, id):
    data = get_child_data(id, request.user)
    if data is None:
        logger.info(f"Unrecognised email {request.user}")
        return redirect("choose")
    return render(request, template_name="portal/dashboard.html", context={"title": "Dashboard", "data": data, "id": data["id"]})


@login_required
def statement_print(request: HttpRequest, id):
    data = get_child_data(id, request.user)

    return render(request, "portal/statement_print.html", {"title": f"Fee Statement - {id}", "id": id, "data": data})


@login_required
def statement(request: HttpRequest, id):
    data = get_child_data(id, request.user)
    data["rows"] = get_statements(id)
    return render(request, "portal/statement.html", {"title": f"Fee Statement - {id}", "id": id, "data": data})

def pay(request: HttpRequest, id):
    data = get_child_data(id, request.user)
    balance = data["balance"]
    balance = balance.replace(",", "")
    if request.method == 'POST':
        phone_number = request.POST.get("phone_no").replace("-", "")
        amount = request.POST.get("amount")
        mpesa = Mpesa()
        try:
            response = mpesa.initiate_stk_push(phone_number, float(amount))
            logger.info(response)
            return render(request, "portal/pay.html", {"title": "Pay Fees", "data": data, "id": id, "message":"Request has been sent to your phone"})
        except Exception as e:
            logger.error(f"An error occured wen initiaiting stk exception '{e}'")
            return render(request, "portal/pay.html", {"title": "Pay Fees", "data": data, "id": id, "message":"Request Failed to Send, Try again later!"})
    return render(request, "portal/pay.html", {"title": "Pay Fees", "data": data, "id": id, "balance":float(balance)})


@login_required
def invite(request: HttpRequest, id):
    data = get_child_data(id, request.user)
    if data is None:
        return redirect("choose")
    if request.method == "POST":
        email = request.POST["email"]
        send_my_email(template="invite", subject="Invitation to the Ark Junior School",
                      recipient=email, user=str(request.user))
        return render(request, "portal/invite.html", {"title": "Invite", "id": id, "data": data, "message": True})
    return render(request, "portal/invite.html", {"title": "Invite", "id": id, "data": data})


# Authentication Views

def login_view(request: HttpRequest):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        parent = authenticate(request, password=password, username=email)
        if parent is not None:
            login(request, user=parent)
            logger.info(f"User {request.user} logged in")
            return redirect("choose")
        return render(request, "portal/login.html", {"title": "Login", "message": "Invalid Email or Password"})
    if request.user.is_anonymous:
        return render(request, "portal/login.html")
    return redirect("choose")


def logout_view(request: HttpRequest):
    logger.info(f"User {request.user} logged out")
    logout(request)
    return redirect("logged_out")


def forgot(request: HttpRequest):
    if request.method == "POST":
        email = request.POST["email"]
        children = [child for child in DB if child["f_email"]
                    == email or child["m_email"] == email]
        no_of_children = len(children)
        if no_of_children > 0:
            user = Parent.objects.filter(username=email).first()
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            reset_url = f'{request.get_host()}/reset/{uidb64}/{token}/'
            send_my_email(template="forgot", subject="Forgot Password",
                          recipient=email, url=reset_url)
            return render(request, "portal/forgot.html", {"success": "Email Sent"})
        return render(request, "portal/forgot.html", {"title": "Forgot Password", "fail": "Invalid Email"})
    return render(request, "portal/forgot.html")


@login_required
def change(request: HttpRequest, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    User = get_user_model()
    user = User.objects.get(pk=uid)
    token_valid = default_token_generator.check_token(user=user, token=token)
    if token_valid:
        return render(request, "portal/change.html", {"title": "Change Password", "uidb64": uidb64, "token": token})
    return redirect("register")


def reset(request: HttpRequest, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    Parent = get_user_model()
    user = Parent.objects.get(pk=uid)
    token_valid = default_token_generator.check_token(user=user, token=token)
    if token_valid:
        context = {"uidb64": uidb64, "token": token}
        return redirect("set_password", **context)
    return redirect("register")


def set_password(request: HttpRequest, uidb64, token):
    if request.method == "POST":
        new_password = request.POST["password"]
        if request.user.is_authenticated:
            request.user.set_password(new_password)
            request.user.save()
            send_my_email(
                template="changed", subject="Password Changed", recipient=str(request.user))
            logger.info(f"Password changed by user {request.user}")
        else:
            uid = force_str(urlsafe_base64_decode(uidb64))
            Parent = get_user_model()
            user = Parent.objects.get(pk=uid)
            user.set_password(new_password)
            user.save()
            send_my_email(template="changed",
                          subject="Password Changed", recipient=str(user))
            logger.info(f"Password reset by user {user.get_username()}")

        # Update the session to avoid requiring reauthentication
        update_session_auth_hash(request, request.user)
        context = {"changed_message": "Password Changed Successfully!"}
        return render(request, 'portal/login.html', context)
    if (request.user.is_authenticated):
        return redirect('proceed')
    else:
        return render(request, "portal/change.html", {"title": "Reset Password", "uidb64": uidb64, "token": token})

        # return render(request, "portal/change.html", {"message":True})



def logged_out(request: HttpRequest):
    return render(request, "portal/logged_out.html", {"title": "Logged Out"})


@login_required
def proceed(request: HttpRequest):
    if request.method == "POST":
        token = default_token_generator.make_token(request.user)
        uidb64 = urlsafe_base64_encode(force_bytes(request.user.id))
        reset_url = f'{request.get_host()}/change/{uidb64}/{token}/'
        send_my_email(template="forgot", subject="Forgot Password",
                      recipient=str(request.user), url=reset_url)
        return render(request, "portal/proceed.html",  {"title": "Send Email", "message": "Email Sent"})
    return render(request, "portal/proceed.html",  {"title": "Send Email"})


def contact(request: HttpRequest):
    return render(request, "portal/contact.html", {"title": "Contact"})


def contact_us(request: HttpRequest):
    return render(request, "portal/contact_us.html", {"title": "Contact Us", })


def modal(request: HttpRequest, id):
    data = get_child_data(id, request.user)
    return render(request, "portal/modal.html", {"title": "Modal Us", "data": data, "id": id})



# HTTP Error 400
def page_not_found(request, exception):
    return render(request, "portal/error_404.html")


def my_bad(request):
    send_my_email("error", "Error 500 on portal website",
                  recipient="atongjonathan@gmail.com")
    return render(request, "portal/error_500.html")
