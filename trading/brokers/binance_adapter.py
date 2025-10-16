from binance.client import Client
from .base import BrokerAdapter

class BinanceAdapter(BrokerAdapter):
    # python-binance Client supports testnet via testnet=True param
    def __init__(self, account):
        super().__init__(account)
        self.api_key = account.get_api_key()
        self.api_secret = account.get_api_secret()
        self.is_demo = account.is_demo
        # Note: python-binance will connect to testnet when testnet=True
        self.client = Client(self.api_key, self.api_secret, testnet=self.is_demo)

    def execute_trade(self, signal_data):
        side = 'BUY' if signal_data.get('side', 'buy').lower() == 'buy' else 'SELL'
        symbol = signal_data.get('symbol')
        qty = signal_data.get('volume')
        # For market orders
        order = self.client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=qty
        )
        # Binance spot doesn't support native TP/SL on market order; OCO or futures required
        return {"status": True, "response": order}
