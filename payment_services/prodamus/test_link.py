import hashlib
import hmac
import json

# from typing import Literal
from collections.abc import MutableMapping
from urllib.parse import urlencode

# from loader import payment 


class ProdamusClient:
    # linktoform = payment.prodamus.link_to_form
    # secret_key = payment.prodamus.secret_key
    linktoform = 'https://christina-astra.payform.ru/'
    secret_key = '657fc2074e897d8f8ac806e0583b30ecbd0f79b64b5e1b213508b68540427e9c'
    
    def generate_link(self):

        data = {
            'order_id': "123556",
            'customer_email': 'housegum@gmail.com',
            'products': [
                {
                    'name': 'artur',
                    'price': '123',
                    'quantity': '1',
                },
            ],
            'customer_extra': 'Dopolnitelniy text',
            'do': 'pay',
            'urlSuccess': 'https://t.me/ChrisMsBot',
            'npd_income_type': 'FROM_INDIVIDUAL',
            'paid_content': 'лололо ты оплатил',
            'callbackType': 'json'
        }

        signature = self._sign(data)
        data['signature'] = signature
        link = self.linktoform + '?' + urlencode(self._http_build_query(data))
        return link

    
    # def make_signature(self, data: dict, secret: str) -> str:
    #     """Алгоритм подписи из Hmac.php / Hmac.js Prodamus"""

    #     def deep_str_and_sort(d):
    #         if isinstance(d, dict):
    #             return {k: deep_str_and_sort(d[k]) for k in sorted(d.keys())}
    #         if isinstance(d, list):
    #             return [deep_str_and_sort(x) for x in d]
    #         return str(d)

    #     clean = deep_str_and_sort(data)
    #     json_str = json.dumps(clean, ensure_ascii=False, separators=(',', ':')).replace('/', '\\/')
    #     return hmac.new(secret.encode(), json_str.encode(), hashlib.sha256).hexdigest()

    def _sign(self, data):

        self._deep_int_to_string(data)
        data_json = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(',', ':')).replace("/", "\\/")
        return hmac.new(self.secret_key.encode('utf8'), data_json.encode('utf8'), hashlib.sha256).hexdigest()

    def _deep_int_to_string(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, MutableMapping):
                self._deep_int_to_string(value)
            elif isinstance(value, list) or isinstance(value, tuple):
                for k, v in enumerate(value):
                    self._deep_int_to_string({str(k): v})
            else: dictionary[key] = str(value)

    def _http_build_query(self, dictionary, parent_key=False):
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

prodamus = ProdamusClient()
print(prodamus.generate_link())
