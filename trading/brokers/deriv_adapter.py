import json
import websocket
import time
from .base import BrokerAdapter

class DerivAdapter(BrokerAdapter):
    DEMO_WS = 'wss://ws.binaryws.com/websockets/v3'
    LIVE_WS = 'wss://ws.derivws.com/websockets/v3'

    def __init__(self, account):
        super().__init__(account)
        self.api_key = account.get_api_key()
        self.base_ws = self.DEMO_WS if account.is_demo else self.LIVE_WS
        # Optionally keep a persistent ws pool externally for performance

    def execute_trade(self, signal_data):
        """
        Very basic Deriv WebSocket flow:
        - authorize
        - send buy/sell proposal/order (this example uses a minimal structure)
        NOTE: adapt to real Deriv API contract proposals in production.
        """
        ws = websocket.create_connection(self.base_ws, timeout=10)
        try:
            # authorize
            auth_msg = {"authorize": self.api_key}
            ws.send(json.dumps(auth_msg))
            # read auth response (not exhaustively handled)
            _ = ws.recv()
            # Build order (this is a simplified example)
            side = signal_data.get('side', 'buy').lower()
            is_buy = 1 if side == 'buy' else 0
            order = {
                "buy": is_buy,
                "amount": signal_data.get('volume', 1),
                "symbol": signal_data.get('symbol', 'R_100'),
                "contract_type": "CALL" if side == 'buy' else "PUT",
            }
            if signal_data.get('sl'):
                order['stop_loss'] = signal_data.get('sl')
            if signal_data.get('tp'):
                order['take_profit'] = signal_data.get('tp')

            ws.send(json.dumps(order))
            response = ws.recv()
            return {"raw": json.loads(response)}
        finally:
            try:
                ws.close()
            except:
                pass
