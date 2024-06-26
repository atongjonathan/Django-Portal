import requests
from logging import getLogger
from .statement_data import get_statements
from datetime import datetime


try:
    from . data import sample_data
except ModuleNotFoundError:
    sample_data = []

sample_data.append({
    "id": "STU-0225",
    "name": "JOHN SMITH",
    "programme": "CBC",
    "stage": "GRADE2T1",
    "no": "",
    "f_name": "CID KAGENOU",
    "f_occupation": "ACCOUNTANT",
    "f_tel": "07123456789",
    "f_email": "test@gmail.com",
    "f_id": "12345678",
    "f_nation": "KENYAN",
    "m_name": "ALPHA SMITH",
    "m_occupation": "TEACHER",
    "m_tel": "0712345678",
    "m_email": "existing@gmail.com",
    "balance": "-3,500.00",
    "billed": "156,000.00",
    "paid": "159,500.00"
})
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
                   for row in student_2023]
    float_credit = [float(row["credit"].replace(',', ''))
                    for row in student_2023]
    balance = sum(float_debit) - sum(float_credit)
    return {"billed": sum(float_debit), "paid": sum(float_credit), "balance": balance}


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

    balance = sum_dict.get("balance")
    subtractions_dict = subtractions(data["rows"])
    billed = subtractions_dict["billed"]
    paid = subtractions_dict["paid"]
    data["bf"] = -(balance - subtractions_dict.get("balance"))
    data["balance"] = balance
    data["billed_perc"] = int(billed/(billed)*100) if billed != 0 else 0
    data["paid_perc"] = int(paid/(billed)*100) if billed != 0 else 0
    data["balance_perc"] = int(balance/(billed)*100) if billed != 0 else 0
    data["billed"] = format(billed, ",.2f")
    data["paid"] = format(paid, ",.2f")
    data["balance"] = format(balance, ",.2f")
    data["bf"] = format(data["bf"], ",.2f")
    return data


def subtractions(data):
    data_2023 = []
    for row in data:
        date_obj = datetime.strptime(row["date"], "%d/%m/%y")
        if date_obj.year == 2023:
            data_2023.append(row)

    return sum_data(data_2023)


DB = real_db()
