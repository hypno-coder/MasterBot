import json, hmac, hashlib, requests

class ProdamusPayment:
    api_url = "https://christina-astra.payform.ru/"
    secret_key = "657fc2074e897d8f8ac806e0583b30ecbd0f79b64b5e1b213508b68540427e9c"

    def generate_link(self, order_id, products, customer_email,
                      url_return='', url_success='', url_notification='', extra_params=None):
        data = {
            "do": "link",
            "order_id": order_id,
            "customer_email": customer_email,
            "products": products,
            "urlReturn": url_return,
            "urlSuccess": url_success,
            "urlNotification": url_notification,
        }
        if extra_params:
            data.update(extra_params)

        self._deep_str(data)
        data["signature"] = self._sign(data)

        response = requests.post(self.api_url, json=data)
        return response

    def _sign(self, data):
        data_json = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).replace("/", "\\/")
        return hmac.new(self.secret_key.encode("utf8"), data_json.encode("utf8"), hashlib.sha256).hexdigest()

    def _deep_str(self, data):
        for k, v in data.items():
            if isinstance(v, dict):
                self._deep_str(v)
            elif isinstance(v, (list, tuple)):
                for i in v:
                    if isinstance(i, dict):
                        self._deep_str(i)
            else:
                data[k] = str(v)

prodamus = ProdamusPayment()
resp = prodamus.generate_link(
    order_id="2134",
    products=[{"name": "TestProduct", "price": "100", "quantity": "1"}],
    customer_email="test@example.com",
    url_notification="https://2saez9-185-255-176-229.ru.tuna.am/payment"
)

print("HTTP:", resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.text)
