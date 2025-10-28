from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


signal_webhook_schema = swagger_auto_schema(
    # method='post',
    manual_parameters=[
        openapi.Parameter(
            'X-USER-KEY',
            openapi.IN_HEADER,
            description="User's secret key",
            type=openapi.TYPE_STRING,
            required=False,
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_email': openapi.Schema(type=openapi.TYPE_STRING, description='User email (optional if X-USER-KEY header is provided)'),
            'broker_account_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the BrokerAccount to execute the signal on'),
            'signal_data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'symbol': openapi.Schema(type=openapi.TYPE_STRING, description='Trading symbol, e.g. BTCUSD'),
                    'side': openapi.Schema(type=openapi.TYPE_STRING, description='"buy" or "sell"'),
                    'volume': openapi.Schema(type=openapi.TYPE_NUMBER, description='Order volume/size'),
                    'sl': openapi.Schema(type=openapi.TYPE_NUMBER, description='Stop loss (optional)'),
                    'tp': openapi.Schema(type=openapi.TYPE_NUMBER, description='Take profit (optional)')
                }
            ),
            'webhook_id': openapi.Schema(type=openapi.TYPE_STRING, description='Unique webhook id for idempotency'),
        },
        required=['broker_account_id', 'signal_data', 'webhook_id'],
        example={
            'user_email': 'trader@example.com',
            'broker_account_id': 1,
            'signal_data': {
                'symbol': 'BTCUSD',
                'side': 'buy',
                'volume': 0.01,
                'sl': 26000,
                'tp': 28000
            },
            'webhook_id': 'uuid-or-unique-string-1234'
        }
    ),
    responses={
        200: openapi.Response(description='Already processed (idempotent)'),
        201: openapi.Response(description='User registered / deprecated for this endpoint'),
        202: openapi.Response(description='Signal accepted and queued for execution'),
        400: openapi.Response(description='Bad request: missing or invalid fields'),
        401: openapi.Response(description='Unauthorized: invalid user key')
    }
)

# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

# @swagger_auto_schema(
#     method='post',
#     manual_parameters=[
#         openapi.Parameter(
#             'X-USER-KEY',
#             openapi.IN_HEADER,
#             description="User's secret key",
#             type=openapi.TYPE_STRING
#         )
#     ],
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'user_email': openapi.Schema(type=openapi.TYPE_STRING),
#             'broker_account_id': openapi.Schema(type=openapi.TYPE_INTEGER),
#             'signal_data': openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     'symbol': openapi.Schema(type=openapi.TYPE_STRING),
#                     'side': openapi.Schema(type=openapi.TYPE_STRING),
#                     'volume': openapi.Schema(type=openapi.TYPE_NUMBER),
#                     'sl': openapi.Schema(type=openapi.TYPE_NUMBER),
#                     'tp': openapi.Schema(type=openapi.TYPE_NUMBER),
#                 }
#             ),
#             'webhook_id': openapi.Schema(type=openapi.TYPE_STRING)
#         },
#         required=['user_email', 'broker_account_id', 'signal_data', 'webhook_id']
#     ),
#     responses={200: 'Signal received'}
# )
# @api_view(['POST'])
# def signal_webhook(request):
#     ...