from django.contrib.auth import get_user_model
from rest_framework.request import Request

User = get_user_model()

def require_user_key(request: Request):
    """
    Validate headers: X-USER-KEY (user.secret_key) and user_email in body or query.
    Returns User instance or None.
    """
    xkey = request.headers.get('X-USER-KEY') or request.META.get('HTTP_X_USER_KEY')
    user_email = request.data.get('user_email') or request.query_params.get('user_email') or request.headers.get('X-USER-EMAIL')
    if not xkey or not user_email:
        return None
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return None
    if user.secret_key != xkey:
        return None
    return user
