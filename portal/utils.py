import requests
import asyncio
import aiohttp
from logging import getLogger

logger = getLogger(__name__)
async def send_my_email_async(template, subject, recipient, url=None, user=None):
    json_data = {
        "subject": subject,
        "recipient": recipient,
        "template": template,
        "url": url,
        "user": user
    }

    async with aiohttp.ClientSession() as session:
        async with session.get("https://atongjona2.pythonanywhere.com/send_email", json=json_data) as response:
            data = await response.json()
            message = str(data.get("message"))
            if message != "Successs":
                logger.info(f"Email was with request {str(json_data)}.\nResponse returned {message}")
            return data

def send_my_email(template, subject, recipient, url=None, user=None):
    # Create an event loop
    loop = asyncio.new_event_loop()

    # Run the asynchronous function in the event loop
    result = loop.run_until_complete(send_my_email_async(template, subject, recipient, url, user))

    # Close the event loop
    loop.close()

    return result

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