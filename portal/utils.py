import requests
from logging import getLogger
from . data import sample_data

logger = getLogger(__name__)


def send_my_email(template, subject, recipient, url=None, user=None):
    json_data = {
        "subject": subject,
        "recipient": recipient,
        "template": template,
        "url": url,
        "user": user
    }
    try:
        response = requests.get(
            "https://atongjona2.pythonanywhere.com/send_email", json=json_data)
        response = response.json()
    except Exception as e:
        logger.error(f"API cannot be reached, exception {e}")
        response = {"message":"API cannot be reached"}
    
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
    DB = sample_data 
    DB = get_avatars(DB)
    return DB


def get_avatars(DB: list):
    for child in DB:
        child["img"] = f"https://ui-avatars.com/api/name={child['name'].replace(' ','+')}?rounded=true&background=random"
    return DB


DB = real_db()
