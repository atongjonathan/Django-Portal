from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Parent
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.http.request import HttpRequest
from django.http import HttpResponse
from portal.utils import *
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages



class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'portal/reset.html'  # Customize this template as needed
    success_url = reverse_lazy('login')  # Redirect to the login page upon successful password reset

    def form_valid(self, form):
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')        
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')        
        response = super().form_invalid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uidb64'] = self.kwargs.get('uidb64')
        context['token'] = self.kwargs.get('token')   

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
        message = f"{request.user} has welcomed you to check out the Ark Junior School."
        print(send_email(email, "Invite to the Ark Junior School", message))
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
            return render(request, "portal/mail_sent.html", {"title": "Proceed ?" })
        return render(request, "portal/forgot.html", {"title": "Forgot Password","message": "Invalid Email" })
    return render(request, "portal/forgot.html")


def recover(request: HttpRequest, uidb64, token):
    return CustomPasswordResetConfirmView.as_view()(request, uidb64=uidb64, token=token)


def set_password(request):
    if request.method == "POST":
        new_password = request.POST["password"]
        request.user.set_password(new_password)
        request.user.save()

        # Update the session to avoid requiring reauthentication
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password changed successfully.')
        return redirect('login')
    else:
        if (request.user):
            return redirect('mail_sent')
        else:
            return redirect("login")

        # return render(request, "portal/reset.html", {"message":True})



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
        reset_url = f'{request.get_host()}/reset-password/{uidb64}/{token}/'
        body = f"Follow this link to reset your password\n {reset_url}"
        send_email(str(request.user)
                    ,"Reset Password", body)
        return render(request, "portal/mail_sent.html", {"message":"Email sent to your inbox"})
    return render(request, "portal/mail_sent.html")


def contact(request: HttpRequest):
    return render(request, "portal/contact.html", {"title": "Contact"})


def contact_us(request: HttpRequest):
    return render(request, "portal/contact_us.html", {"title": "Contact Us", })

def modal(request: HttpRequest, id):
    data = get_child_data(id, request.user)
    return render(request, "portal/modal.html", {"title": "Modal Us","data":data, "id":id })


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
