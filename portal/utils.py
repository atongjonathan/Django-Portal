import requests


EMAILS = {
    "new_login":
    {
        "subject":"Welcome to The Ark Junior Parents Portal - Your New Login Details",
        "body":"""
        Dear Parent,

        We are excited to welcome you to the Parents Portal! Your login details are confirmed, and you can access the portal at your own convinience 

        Please log in at the Parents Portal and explore the various features available to keep track of your child's academic progress, fees status, and stay updated with school announcements.

        If you have any questions or need assistance, feel free to contact our support team at <portal@thearkjuniorschool.com>
>
        Best regards,
        """
    },
        "password_reset":
    {
        "subject":"Portal - Password Reset",
        "body":"""
        Dear Parent,

        This is to confirm that your password for the [School Name] Portal has been successfully reset. If you did not request this change, please contact our support team immediately.

        You can log in with your email and the new password. 

        If you need further assistance, please don't hesitate to reach out to our support team at <portal@thearkjuniorschool.com>.

        Best regards,
        """
    },

}

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