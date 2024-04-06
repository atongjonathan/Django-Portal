import requests
from logging import getLogger
# try:
from . data import sample_data
# except ModuleNotFoundError:
#     from . example_data import sample_data

from .statement_data import get_statements


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
        response = {"message": "API cannot be reached"}

    message = response.get("message")
    if message != "Success":
        logger.error(f"Email Sending failed with response {message}")
    else:
        logger.info(f"Email Sent from json {json_data}")
    return response


def sum_data(student_2023):
    float_debit = [float(row["debit"].replace(',', ''))
                   for row in student_2023 if row["debit"] != ""]
    float_credit = [float(row["credit"].replace(',', ''))
                    for row in student_2023 if row["credit"] != ""]
    return {"billed": sum(float_credit), "paid": sum(float_debit)}


def get_child_data(id, user):
    for child in DB:
        if child["id"] == id and (child["f_email"] == str(user) or child["m_email"] == str(user)):
            statements = get_statements(id)
            child["rows"] = statements
            child = get_data(child)
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


def get_data(data: dict):
    # print(data)
    sum_dict = sum_data(data["rows"])
    data["billed"] = sum_dict.get("billed")
    data["paid"] = sum_dict.get("paid")
    billed = data["billed"]
    paid = data["paid"]
    balance = billed - paid
    data["balance"] = balance
    data["billed_perc"] = int(billed/(billed)*100)
    data["paid_perc"] = int(paid/(billed)*100)
    data["balance_perc"] = int(balance/(billed)*100)
    data["billed"] = format(billed, ",.2f")
    data["paid"] = format(paid, ",.2f")
    data["balance"] = format(balance, ",.2f")
    return data


DB = real_db()
