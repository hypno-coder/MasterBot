import json
from decimal import Decimal
import hashlib
from urllib import parse

from loader import payment as p
from database.connector import redis_db
from ..user_data_type import UserDataType


def calculate_signature(*args) -> str:
    '''Create signature MD5.
    '''
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


def check_signature_result(
    order_number: int,  # invoice number
    received_sum: Decimal,  # cost of goods, RU
    received_signature: str,  # SignatureValue
    password: str = p.robokassa.password_1,
) -> bool:
    signature = calculate_signature(received_sum, order_number, password)

    if signature.lower() == received_signature.lower():
        return True
    return False


# Формирование URL переадресации пользователя на оплату.
def generate_payment_link(
    cost: Decimal,  # Cost of goods, RU
    number: int,  # Invoice number
    description: str,  # Description of the purchase
    user_data: UserDataType,
    merchant_password_1: str = p.robokassa.password_1,
    merchant_login: str = p.robokassa.merchant_login,  # Merchant login
    is_test = p.robokassa.is_test,
    robokassa_payment_url = 'https://auth.robokassa.ru/Merchant/Index.aspx',
) -> str:
    '''URL for redirection of the customer to the service.
    '''
    receipt = {
          'sno':'usn_income',
          'items': [
            {
              'name': description,
              'quantity': 1,
              'sum': str(cost),
              'payment_method': 'full_payment',
              'payment_object': 'service',
              'tax': 'vat0'
            }]}
            
    receipt_json = json.dumps(receipt)
    receipt_encoded = parse.quote(receipt_json)

    signature = calculate_signature(
        merchant_login,
        cost,
        number,
        receipt_encoded,
        merchant_password_1
    )

    data = {
        'MerchantLogin': merchant_login,
        'OutSum': cost,
        'InvId': number,
        'Description': description,
        'SignatureValue': signature,
        'Receipt': receipt_encoded,
        'IsTest': is_test
    }

    redis_db.setex(str(number), 6000, json.dumps(user_data))
    return f'{robokassa_payment_url}?{parse.urlencode(data)}'

