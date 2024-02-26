import requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_my_email(template, subject, recipient, url=None, user=None):
    if template == "forgot":
        url = f"https://{url}"
        html_message = render_to_string(template_name=f"emails/{template}.html", context={"link":url})
    elif template == "invite":
        html_message = render_to_string(template_name=f"emails/{template}.html", context={"user":user})
    else:
        html_message = render_to_string(template_name=f"emails/{template}.html")
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
    to=[recipient],
        from_email="portal@thearkjuniorschool.com",
        subject=subject,
        body=plain_message
    )
    message.attach_alternative(html_message, "text/html")
    try:
        message.send(fail_silently=False)
        print("Email Sent to", recipient)
        return True
    except Exception as e:
        print(e)
        return False


def get_child_data(id, user):
    for child in DB:
        if child["id"] == id and (child["f_email"] == str(user) or child["m_email"] == str(user)):
            return child
    return None

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


global DB
DB = real_db()