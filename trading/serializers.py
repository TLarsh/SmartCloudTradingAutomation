from rest_framework import serializers
from .models import User, BrokerAccount

from .utils import encrypt_text

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = (
            'email',
            'password', 
            'full_name'
            )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data.pop('password', None),
            full_name=validated_data.get('full_name', '')
        )
        return user

# class BrokerAccountSerializer(serializers.ModelSerializer):
#     api_key = serializers.CharField(write_only=True)
#     api_secret = serializers.CharField(write_only=True, required=False, allow_blank=True)
#     is_demo = serializers.BooleanField(default=True)
#     user_email = serializers.CharField(write_only=True)

#     class Meta:
#         model = BrokerAccount
#         fields = ('provider', 'display_name', 'api_key', 'api_secret', 'user_email', 'is_demo')

#     def create(self, validated_data):
#         request = self.context.get('request')
#         email = validated_data.get('user_email')
#         user = User.objects.get(email=email)
#         # user = request.user
#         account = BrokerAccount(
#             user=user,
#             provider=validated_data['provider'],
#             display_name=validated_data['display_name'],
#             is_demo=validated_data.get('is_demo', True)
#         )
#         api_key = validated_data.get('api_key')
#         api_secret = validated_data.get('api_secret', None)
#         account.set_api_key(api_key, api_secret)
#         account.save()
#         return account




class BrokerAccountSerializer(serializers.ModelSerializer):
    encrypted_api_key = serializers.CharField(write_only=True)
    user_email = serializers.CharField(write_only=True)
    

    class Meta:
        model = BrokerAccount
        fields = ('provider', 'display_name', 'encrypted_api_key', 'user_email', 'is_demo')

    def create(self, validated_data):
      
        encrypted_api_key = validated_data.pop('encrypted_api_key'),
        validated_data['_encrypted_api_key'] = encrypt_text(encrypted_api_key)
  


        return super().create(validated_data)
    
class ListBrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokerAccount
        fields = [
            'id',
            'provider',
            'display_name',
            'encrypted_api_key',
            'encrypted_api_secret',
            'user',
            'is_demo',
            'created_at'
        ]

