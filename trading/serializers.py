from rest_framework import serializers
from .models import User, BrokerAccount

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'full_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', '')
        )
        return user

class BrokerAccountSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(write_only=True)
    api_secret = serializers.CharField(write_only=True, required=False, allow_blank=True)
    is_demo = serializers.BooleanField(default=True)

    class Meta:
        model = BrokerAccount
        fields = ('provider', 'display_name', 'api_key', 'api_secret', 'is_demo')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        account = BrokerAccount(
            user=user,
            provider=validated_data['provider'],
            display_name=validated_data['display_name'],
            is_demo=validated_data.get('is_demo', True)
        )
        api_key = validated_data.get('api_key')
        api_secret = validated_data.get('api_secret', None)
        account.set_api_key(api_key, api_secret)
        account.save()
        return account
