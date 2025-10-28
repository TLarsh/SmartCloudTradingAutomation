from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from ..serializers import BrokerAccountSerializer

broker_register_schema = swagger_auto_schema(
    manual_parameters=[
        openapi. Parameter(
            'X-USER-KEY',
            openapi.IN_HEADER,
            description="User's secret key",
            type=openapi.TYPE_STRING
        )
    ],
    request_body= BrokerAccountSerializer
)