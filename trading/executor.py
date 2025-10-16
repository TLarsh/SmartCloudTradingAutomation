from .brokers.deriv_adapter import DerivAdapter
from .brokers.exness_adapter import ExnessAdapter
from .brokers.oanda_adapter import OandaAdapter
from .brokers.binance_adapter import BinanceAdapter

def get_broker_adapter(account):
    provider = account.provider.lower()
    if provider == 'deriv':
        return DerivAdapter(account)
    elif provider == 'exness':
        return ExnessAdapter(account)
    elif provider == 'oanda':
        return OandaAdapter(account)
    elif provider == 'binance':
        return BinanceAdapter(account)
    else:
        raise ValueError(f"Unsupported provider: {provider}")
