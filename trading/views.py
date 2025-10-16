from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, BrokerAccountSerializer
from .models import Signal, BrokerAccount
from .utils import require_user_key
from .tasks import process_signal_task

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "Validation failed", "status": False, "data": None, "errors": serializer.errors}, status=400)
        user = serializer.save()
        return Response({"message": "User registered", "status": True, "data": {"email": user.email, "secret_key": user.secret_key}, "errors": None}, status=201)

class AddBrokerView(APIView):
    """
    Requires header X-USER-KEY and user_email (in body or header)
    """
    def post(self, request):
        user = require_user_key(request)
        if not user:
            return Response({"message":"Unauthorized", "status":False, "data":None, "errors":"Invalid credentials"}, status=401)
      
        request._cached_user = user  
        serializer = BrokerAccountSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response({"message":"Validation failed","status":False,"data":None,"errors":serializer.errors}, status=400)
        account = serializer.save()
        return Response({"message":"Broker account added","status":True,"data":{"id":account.id,"provider":account.provider,"display_name":account.display_name},"errors":None}, status=201)

class SignalWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
        user = require_user_key(request)
        if not user:
            return Response({"message":"Unauthorized", "status":False, "data":None, "errors":"Invalid credentials"}, status=401)

        webhook_id = request.data.get('webhook_id')
        if not webhook_id:
            return Response({"message":"Missing webhook_id","status":False,"data":None,"errors":"Provide webhook_id for idempotency"}, status=400)

        
        payload = request.data
        signal, created = Signal.objects.get_or_create(webhook_id=webhook_id, user=user, defaults={'payload': payload})
        if not created:
            
            return Response({"message":"Already processed (idempotent)","status":True,"data":{"webhook_id":webhook_id},"errors":None}, status=200)

        
        broker_account_id = payload.get('broker_account_id')
        signal_data = payload.get('signal_data') or {}

        if not broker_account_id or not signal_data:
            
            signal.processed = True
            signal.result = {'status': False, 'message': 'Missing broker_account_id or signal_data'}
            signal.save()
            return Response({"message":"Missing data","status":False,"data":None,"errors":"broker_account_id and signal_data required"}, status=400)

        
        process_signal_task.delay(user.id, broker_account_id, signal.id)

        return Response({"message":"Signal accepted and queued for execution","status":True,"data":{"webhook_id":webhook_id},"errors":None}, status=202)
