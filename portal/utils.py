import requests
import asyncio
import aiohttp
from asgiref.sync import sync_to_async


def send_email(receiver, subject, body):
    url = "https://atongjona2.pythonanywhere.com/send_email"
    payload = {
        "recipient_email": receiver,
        "subject": subject,
        "body": body
    }
    response = requests.get(url, json=payload)
    return response.json()


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