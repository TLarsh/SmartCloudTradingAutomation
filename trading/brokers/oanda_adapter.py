import requests
from .base import BrokerAdapter

class OandaAdapter(BrokerAdapter):
    DEMO_URL = 'https://api-fxpractice.oanda.com/v3'
    LIVE_URL = 'https://api-fxtrade.oanda.com/v3'

    def __init__(self, account):
        super().__init__(account)
        self.api_key = account.get_api_key()
        # We store the OANDA account ID in encrypted_api_secret
        self.account_id = account.get_api_secret()
        self.base_url = self.DEMO_URL if account.is_demo else self.LIVE_URL
        self.headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}

    def execute_trade(self, signal_data):
        side = signal_data.get('side', 'buy').lower()
        units = signal_data.get('volume', 1)
        # OANDA expects positive or negative units depending on direction
        if side == 'sell':
            units = -abs(units)
        data = {
            "order": {
                "units": str(units),
                "instrument": signal_data.get('symbol'),
                "type": "MARKET",
            }
        }
        # optional SL/TP on fill
        if signal_data.get('sl'):
            data['order']['stopLossOnFill'] = {"price": str(signal_data.get('sl'))}
        if signal_data.get('tp'):
            data['order']['takeProfitOnFill'] = {"price": str(signal_data.get('tp'))}

        url = f"{self.base_url}/accounts/{self.account_id}/orders"
        resp = requests.post(url, json=data, headers=self.headers, timeout=10)
        try:
            body = resp.json()
        except Exception:
            body = {"text": resp.text}
        return {"status": resp.ok, "http_status": resp.status_code, "response": body}
