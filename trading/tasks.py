from celery import shared_task
from django.utils import timezone
from .models import Signal, BrokerAccount
from .executor import get_broker_adapter
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_signal_task(self, user_id, broker_account_id, signal_id):
    """
    This task loads the signal from DB, picks the broker account and executes the trade.
    signal_id: DB ID of Signal (so signal.payload remains available)
    """
    try:
        signal = Signal.objects.get(id=signal_id)
    except Signal.DoesNotExist:
        logger.error("Signal not found: %s", signal_id)
        return {"status": False, "message": "Signal not found"}

    payload = signal.payload
    
    try:
        account = BrokerAccount.objects.get(id=broker_account_id, user_id=user_id)
    except BrokerAccount.DoesNotExist:
        signal.processed = True
        signal.result = {"status": False, "message": "Broker account not found"}
        signal.save()
        return signal.result

    adapter = get_broker_adapter(account)

    signal_data = payload.get('signal_data') or {}

    try:
        result = adapter.execute_trade(signal_data)
        signal.processed = True
        signal.result = {"status": True, "response": result, "executed_at": timezone.now().isoformat()}
        signal.save()
        return signal.result
    except Exception as exc:
        logger.exception("Trade execution failed for signal %s: %s", signal_id, exc)
        # retry with exponential backoff
        try:
            self.retry(exc=exc, countdown=10)
        except self.MaxRetriesExceededError:
            signal.processed = True
            signal.result = {"status": False, "message": str(exc)}
            signal.save()
            return signal.result
