import os
from celery import Celery

# Ensure the Django settings module is set before creating the Celery app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCloudTradingAutomation.settings')

# Create the Celery app using the Django project name. Export both `app` and
# `celery` so the Celery CLI can import the package and find the expected
# attribute (some invocations look for `celery` specifically).
app = Celery('SmartCloudTradingAutomation')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Aliases for CLI discovery
celery = app
