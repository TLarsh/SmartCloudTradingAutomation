from .celery import app as celery_app

# Expose commonly-used attributes so `celery -A SmartCloudTradingAutomation worker`
# can locate the application. Celery looks for 'celery' attribute on the package
# by default; some setups also expect 'app'. We keep 'celery_app' for Django
# conventions and add aliases.
celery = celery_app
app = celery_app

__all__ = ('celery_app', 'celery', 'app')
