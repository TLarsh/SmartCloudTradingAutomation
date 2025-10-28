from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from ..serializers import RegisterSerializer

user_register_schema = swagger_auto_schema(
    request_body= RegisterSerializer
)