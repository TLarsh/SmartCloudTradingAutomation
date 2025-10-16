# from .base import BrokerAdapter
# import requests

# class ExnessAdapter(BrokerAdapter):
#     DEMO_URL = "https://demo-api.exness.com"
#     LIVE_URL = "https://api.exness.com"

#     def __init__(self, account):
#         super().__init__(account)
#         self.api_key = account.get_api_key()
#         self.base_url = self.DEMO_URL if account.is_demo else self.LIVE_URL

#     def buy(self, symbol, volume, sl=None, tp=None):
#         payload = {
#             "symbol": symbol,
#             "volume": volume,
#             "side": "buy",
#             "sl": sl,
#             "tp": tp
#         }
#         return self._send_order(payload)
    
#     def sell(self, symbol, volume, sl=None, tp=None):
#         payload = {
#             "symbol": symbol,
#             "volume": volume,
#             "side": "sell",
#             "sl": sl,
#             "tp": tp,
#         }
#         return self._send_order(payload)
    
#     def _send_order(self, payload):
#         headers = {"Authorization": f"Bearer {self.api_key}"}
#         response = requests.post(f"{self.base_url}/trade", json=payload, headers=headers)
#         return response.json()
    


import requests
from .base import BrokerAdapter

class ExnessAdapter(BrokerAdapter):
    DEMO_URL = "https://demo-api.exness.com"
    LIVE_URL = "https://api.exness.com"

    def __init__(self, account):
        super().__init__(account)
        self.api_key = account.get_api_key()
        self.base_url = self.DEMO_URL if account.is_demo else self.LIVE_URL
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def execute_trade(self, signal_data):
        payload = {
            "symbol": signal_data.get('symbol'),
            "volume": signal_data.get('volume'),
            "side": signal_data.get('side'),
        }
        if signal_data.get('sl') is not None:
            payload['sl'] = signal_data.get('sl')
        if signal_data.get('tp') is not None:
            payload['tp'] = signal_data.get('tp')

        # Exness endpoint paths vary by account type and product; this is an example
        url = f"{self.base_url}/trade"
        resp = requests.post(url, json=payload, headers=self.headers, timeout=10)
        try:
            data = resp.json()
        except Exception:
            data = {"text": resp.text}
        return {"status": resp.ok, "http_status": resp.status_code, "response": data}

