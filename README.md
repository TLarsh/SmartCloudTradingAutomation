- How to run (local, minimal)

Create virtualenv, install requirements:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


- Ensure Postgres and Redis are running (local or remote). Configure env vars accordingly.

Run migrations:

python manage.py makemigrations
python manage.py migrate


- Create superuser (optional):

python manage.py createsuperuser


- Start Django server:

python manage.py runserver 0.0.0.0:8000


- Start Celery worker (in another terminal):

celery -A model1 worker --loglevel=info


- (Optional) Start Flower for Celery monitoring:

pip install flower
celery -A model1 flower