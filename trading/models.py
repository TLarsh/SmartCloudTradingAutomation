from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from cryptography.fernet import Fernet

def _get_fernet():
    key = settings.FERNET_KEY
    if isinstance(key, str):
        key = key.encode()
    return Fernet(key)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        import secrets
        user.secret_key = secrets.token_urlsafe(32)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    secret_key = models.CharField(max_length=128, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class BrokerAccount(models.Model):
    PROVIDER_CHOICES = [
        ('deriv', 'Deriv'),
        ('oanda', 'OANDA'),
        ('binance', 'Binance'),
        ('exness', 'Exness'),
    ]
    user = models.ForeignKey(User, related_name='broker_accounts', on_delete=models.CASCADE)
    provider = models.CharField(max_length=64, choices=PROVIDER_CHOICES)
    display_name = models.CharField(max_length=128)
    encrypted_api_key = models.TextField()
    encrypted_api_secret = models.TextField(blank=True, null=True)
    is_demo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_api_key(self, api_key, api_secret=None):
        f = _get_fernet()
        self.encrypted_api_key = f.encrypt(api_key.encode()).decode()
        if api_secret is not None:
            self.encrypted_api_secret = f.encrypt(api_secret.encode()).decode()

    def get_api_key(self):
        f = _get_fernet()
        return f.decrypt(self.encrypted_api_key.encode()).decode()

    def get_api_secret(self):
        if not self.encrypted_api_secret:
            return None
        f = _get_fernet()
        return f.decrypt(self.encrypted_api_secret.encode()).decode()

    def __str__(self):
        return f"{self.display_name} ({self.provider})"

class Signal(models.Model):
    webhook_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    result = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Signal {self.webhook_id} for {self.user.email}"
