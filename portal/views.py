from django.shortcuts import render



def register(request):
    if request.method == 'POST':
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm_password"]
    elif request.method == "GET":
        pass

    return render(request, "portal/register.html")

def login(request):
    return render(request, "portal/login.html")

def forgot(request):
    return render(request, "portal/forgot.html")

def recover(request):
    return render(request, "portal/recover.html")
def dashboard(request):
    return render(request, template_name="portal/dashboard.html")


def test(request):
    return render(request, 'portal/test.html')