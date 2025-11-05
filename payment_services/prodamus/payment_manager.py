import hashlib
import hmac
import json
from collections.abc import MutableMapping
from typing import Literal
from urllib.parse import urlencode

from payment_services.user_data_type import UserDataType
from loader import payment
from database.connector import redis_db

class ProdamusClient:
    linktoform: str = payment.prodamus.link_to_form
    secret_key: str = payment.prodamus.secret_key

    def __init__(self, mode: Literal["link", "webhook"]):
        self.mode = mode
    
    def generate_link(
            self, 
            order_id: str,
            price: str,
            name: str,
            user_data: UserDataType
    ) -> str:

        data = {
            'order_id': order_id,
            'products': [
                {
                    'name': name ,
                    'price': price,
                    'quantity': '1',
                    'type': 'service'
                },
            ],
            'customer_extra': "Обязательно укажите Email, на него прийдет чек",
            'do': 'pay',
            'urlSuccess': 'https://t.me/ChrisMsBot',
            'npd_income_type': 'FROM_INDIVIDUAL',
            'paid_content': 'Оплата прошла успешно, результат можно получить по этой ссылке: https://t.me/MasterAstraBot',
            'callbackType': 'json',
            '_param_id': order_id
        }
        redis_db.setex(order_id, 6000, json.dumps(user_data))
        signature = self.make_signature(data)
        data['signature'] = signature
        link = self.linktoform + '?' + urlencode(self._http_build_query(data))
        return link

    def make_signature(self, data: dict) -> str:
        match self.mode:
            case "link":
                self._deep_int_to_string(data)
                payload = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
            case "webhook":
                clean = self._deep_str_and_sort(data)
                payload = json.dumps(clean, ensure_ascii=False, separators=(",", ":"))
            case _:
                raise ValueError("Invalid mode") 

        payload = payload.replace("/", "\\/")
        return hmac.new(self.secret_key.encode("utf8"), payload.encode("utf8"), hashlib.sha256).hexdigest()
    
    def _deep_int_to_string(self, d) -> None:
        for k, v in d.items():
            if isinstance(v, MutableMapping):
                self._deep_int_to_string(v)
            elif isinstance(v, (list, tuple)):
                for i, x in enumerate(v):
                    self._deep_int_to_string({str(i): x})
            else:
                d[k] = str(v)

    def _deep_str_and_sort(self, d) -> str | list | dict:
        if isinstance(d, dict):
            return {k: self._deep_str_and_sort(d[k]) for k in sorted(d.keys())}
        if isinstance(d, list):
            return [self._deep_str_and_sort(x) for x in d]
        return str(d)
        

    def _http_build_query(self, dictionary, parent_key=False) -> dict:
        items = []
        for key, value in dictionary.items():
            new_key = str(parent_key) + '[' + key + ']' if parent_key else key
            if isinstance(value, MutableMapping):
                items.extend(self._http_build_query(value, new_key).items())
            elif isinstance(value, list) or isinstance(value, tuple):
                for k, v in enumerate(value):
                    items.extend(self._http_build_query({str(k): v}, new_key).items())
            else:
                items.append((new_key, value))
        return dict(items)
