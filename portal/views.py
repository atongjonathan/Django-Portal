from django.shortcuts import render, redirect
from .models import Parent
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.http.request import HttpRequest
from django.http import HttpResponse
from portal.utils import *


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
        return render(request, "portal/choose.html", {"title": "Choose Child", "children": children})


@login_required
def dashboard(request: HttpRequest, id):
    data = get_child_data(id, request.user)
    if data is None:
        return render(request, "portal/choose.html", {"title": "Dashboard", "message": " Your email is not recognised by the school. Visit school to update!"})
    return render(request, template_name="portal/dashboard.html", context={"data": data, "id": data["id"]})


@login_required
def statement_print(request: HttpRequest, id):
    data = get_child_data(id, request.user)
    return render(request, "portal/statement_print.html", {"title": "Fee Statement", "id": id, "data": data})


@login_required
def statement(request: HttpRequest, id):
    for child in DB:
        if child["id"] == id and (child["f_email"] == str(request.user) or child["m_email"] == str(request.user)):
            data = child
            return render(request, "portal/statement.html", {"title": "Fee Statement", "id": id, "data": data})

@login_required
def invite(request: HttpRequest, id):
    data = get_child_data(id, request.user)
    if request.method == "POST":
        email = request.POST["email"]
        message = f"Subject: Invite to the Ark Junior School\n\n{request.user} Welcomes you to check out the Ark Junior Schools"
        print(send_email(settings.EMAIL_HOST, email, message))
        return render(request, "portal/invite.html", {"title": "Invite", "id": id, "data": data, "message": True})
    return render(request, "portal/invite.html", {"title": "Invite", "id": id, "data": data})

@login_required
def structure(request: HttpRequest):
    return render(request, "portal/structure.html", {"title": "Fee Structure", })


# Authentication Views

def login_view(request: HttpRequest):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        parent = authenticate(request, password=password, username=email)
        if parent is not None:
            login(request, user=parent)
            return redirect("choose")
        else:
            return render(request, "portal/login.html", {"title": "Fee Statement", "message": "Invalid Email or Password"})
    else:
        if (request.user.is_anonymous):
            return render(request, "portal/login.html")
        else:
            return redirect("choose")


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("logged_out")


def forgot(request: HttpRequest):
    if request.method == "POST":
        email = request.POST["email"]
        parent = Parent.objects.filter(username=email).first()
        if parent:
            # Generate a token and send an email

            return redirect("recover")
    return render(request, "portal/forgot.html", {"title": "Forgot Password", })


def recover(request: HttpRequest):
    return render(request, "portal/reset.html", {"title": "Change Password", })


def test(request: HttpRequest):
    return render(request, 'portal/test.html')

# Looged Out Views

def logged_out(request: HttpRequest):
    return render(request, "portal/logged_out.html", {"title": "Logged Out", })


@login_required
def mail_sent(request: HttpRequest):
    if request.method == "POST":
        token = default_token_generator.make_token(request.user)
        uidb64 = urlsafe_base64_encode(force_bytes(request.user.id))
        reset_url = f'{request.get_host}/reset-password/{uidb64}/{token}/'
        send_email(str(request.user)
                    ,"Reset Password", reset_url)
        return HttpResponse("Email Sent")
    return render(request, "portal/mail_sent.html")


def contact(request: HttpRequest):
    return render(request, "portal/contact.html", {"title": "Contact"})


def contact_us(request: HttpRequest):
    return render(request, "portal/contact_us.html", {"title": "Contact Us", })


# HTTP Error 400
def page_not_found(request, exception):
    return render(request, "portal/error_404.html")


# def statement(request, id):
#     for child in DB:
#         if child["id"] == id and (child["f_email"] == str(request.user) or child["m_email"] == str(request.user)):
#             data = child

#             buffer = BytesIO()
#             p = canvas.Canvas(buffer)

#             # Add your content using ReportLab's API
#             # Example: Draw text at specific coordinates
#             content = render_to_string("portal/statement_print.html", {"title": "Fee Statement - PDF", "id": id, "data": data})
#             p.drawString(100, 100, content)  # Replace with your content and formatting
#             p.save()
#             buffer.seek(0)
#             filename = f"fee_statement_{id}.pdf"
#             with open(filename, 'wb') as pdf_file:
#                 pdf_file.write(buffer.read())
#             with open(filename, 'rb') as pdf_file:
#                 response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#                 response['Content-Disposition'] = f'attachment; filename="{filename}"'
#             return response

#     # Handle the case where no matching child is found
#     return HttpResponse("Child not found")
