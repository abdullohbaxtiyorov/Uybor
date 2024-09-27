from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import Serializer, ModelSerializer
from .models import User





class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'user_type', 'photo', 'is_phone_verified']

class RegisterUserSerializer(Serializer):
    phone_number = IntegerField(help_text='Phone number')

class VerifySerializer(Serializer):
    phone_number = CharField(max_length=11)
    code = CharField(max_length=8)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        code = attrs.get('code')
        cache_code = str(cache.get(phone_number))
        if code != cache_code:
            raise ValidationError({'code': 'Code not found or timed out'})
        return attrs
