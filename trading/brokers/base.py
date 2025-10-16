class BrokerAdapter:
    def __init__(self, account):
        self.account = account


def execute_trade(self, signal_data):
    raise NotImplementedError("execute_trade must be implemented")


def modify_trade(self, signal_data):
    raise NotImplementedError("modify_trade must be implemented")



class BrokerAdapter:
    def __init__(self, account):
        self.account = account

    def execute_trade(self, signal_data):
        """
        Implement placing a trade: side, symbol, volume, sl, tp
        Return a dict-like response
        """
        raise NotImplementedError

    def modify_trade(self, signal_data):
        raise NotImplementedError
