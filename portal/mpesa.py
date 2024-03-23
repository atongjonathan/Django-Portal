import requests
import base64
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from django.conf import settings
print(load_dotenv())

class Mpesa():
    def __init__(self) -> None:
        # test_3 = json.loads(os.environ.get("test_3"))
        test_3 = {"consumer_key": "AitjEGY0rigIzv49I6EafK9e4MyC1KNoPHDKPGaGb8zo6hKo","consumer_secret": "JIWXWCzXjXbRUcnpT5bbz9SB1tzxehH9tL4A69XuGnr2AqWsjd1a5qv0vRqmevwA"}
        self.headers = self.get_headers(test_3)


    def get_access_token(self, credentials: dict):
        access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        headers = {'Content-Type': 'application/json'}
        auth = (credentials.get("consumer_key"),
                credentials.get("consumer_secret"))
        response = requests.get(access_token_url, headers=headers, auth=auth)
        response.raise_for_status()
        result = response.json()
        access_token = result['access_token']
        return access_token

    def bearer_header(self, credentials:dict):
        access_token = self.get_access_token(credentials)
        headers = {
        "Authorization": f"Bearer " + access_token,
        'Content-Type': 'application/json'}
        return headers


    def get_headers(self, credentials:dict):
        try:
            access_token = self.get_access_token(credentials)
            settings.ACCESS_TOKEN = access_token
        except Exception as e:
            access_token = settings.ACCESS_TOKEN

        headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
        "X-appKey": credentials.get("consumer_key")
    }
        return headers




    def initiate_stk_push(self, PHONE_NO, amount):
        print(self.headers)
        # amount = 1
        phone = PHONE_NO
        passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        business_short_code = '174379'
        process_request_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        callback_url = 'https://atongjona2.pythonanywhere.com/'
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            (business_short_code + passkey + timestamp).encode()).decode()
        party_a = phone
        account_reference = "Parent's Portal"
        transaction_desc = "Test"

        json = {
            'BusinessShortCode': business_short_code,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',#  The transaction type for M-PESA Express is "CustomerPayBillOnline" for PayBill Numbers and "CustomerBuyGoodsOnline" for Till Numbers
            'Amount': amount,
            'PartyA': party_a, # The phone number sending money in the format 2547XXXXXXXX
            'PartyB': business_short_code, # The organization that receives the funds.
            'PhoneNumber': party_a, # The Mobile Number to receive the STK Pin Prompt
            'CallBackURL': callback_url,
            'AccountReference': account_reference, # Identifier of the transaction for the CustomerPayBillOnline transaction type. Along with the business name, this value is also displayed to the customer in the STK Pin Prompt message
            'TransactionDesc': transaction_desc # Any additional information/comment that can be sent along with the request from your system
        }

        response = requests.post(process_request_url, headers=self.headers, json=json)
        response_data = response.json()
        return response_data


    def query_status(self, requestID):
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
        passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        business_short_code = '174379'
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(
            (business_short_code + passkey + timestamp).encode()).decode()
        json = {
            "BusinessShortCode": "174379",
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": requestID,
        }
        response = requests.post(api_url, json=json, headers=self.headers)
        return response.json()


# print(initiate_stk_push())
# print(query_status("ws_CO_12032024091213124708683896"))



