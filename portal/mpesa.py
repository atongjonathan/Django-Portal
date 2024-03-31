import requests
import base64
from datetime import datetime
from django.conf import settings
import json
from logging import getLogger

logger = getLogger(__name__)


class Mpesa():
    def __init__(self) -> None:
        self.headers = self.get_headers(
            json.loads(settings.DARAJA_CREDENTIALS))

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

    def bearer_header(self, credentials: dict):
        access_token = self.get_access_token(credentials)
        headers = {
            "Authorization": f"Bearer " + access_token,
            'Content-Type': 'application/json'}
        return headers

    def get_headers(self, credentials: dict):
        access_token = settings.ACCESS_TOKEN
        try:
            access_token = self.get_access_token(credentials)
            settings.ACCESS_TOKEN = access_token
            logger.info(f"No issues getting access token, i.e {access_token}")
        except Exception as e:
            logger.error(
                f"An issue occurred when getting access token  with exception {e}.Thus using settings access token i.e {access_token}")
            

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
            "X-appKey": credentials.get("consumer_key")
        }
        return headers

    def initiate_stk_push(self, PHONE_NO, amount):
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
            # The transaction type for M-PESA Express is "CustomerPayBillOnline" for PayBill Numbers and "CustomerBuyGoodsOnline" for Till Numbers
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': party_a,  # The phone number sending money in the format 2547XXXXXXXX
            # The organization that receives the funds.
            'PartyB': business_short_code,
            'PhoneNumber': party_a,  # The Mobile Nmber to receive the STK Pin Prompt
            'CallBackURL': callback_url,
            # Identifier of the transaction for the CustomerPayBillOnline transaction type. Along with the business name, this value is also displayed to the customer in the STK Pin Prompt message
            'AccountReference': account_reference,
            # Any additional information/comment that can be sent along with the request from your system
            'TransactionDesc': transaction_desc
        }
        try:
            response = requests.post(
                process_request_url, headers=self.headers, json=json)
        except Exception as e:
            self.logger.error(f"An error occured when calling stkpush api {e}")
        try:
            response_data = response.json()
            return response_data
        except Exception as e:
            self.logger(f"An error occured in accessing json response {e}")

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