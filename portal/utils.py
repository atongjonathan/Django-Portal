import requests
from logging import getLogger

logger = getLogger(__name__)


def send_my_email(template, subject, recipient, url=None, user=None):
    json_data = {
        "subject": subject,
        "recipient": recipient,
        "template": template,
        "url": url,
        "user": user
    }

    response = requests.get(
        "https://atongjona2.pythonanywhere.com/send_email", json=json_data)
    response = response.json()
    message = response.get("message")
    if message != "Success":
        logger.error(f"Email Sending failed with response {message}")
    else:
        logger.info(f"Email Sent from json {json_data}")
    return response


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
        child["img"] = f"https://ui-avatars.com/api/name={child['name'].replace(' ','+')}?rounded=true&background=random"
    return DB


global DB
DB = real_db()
