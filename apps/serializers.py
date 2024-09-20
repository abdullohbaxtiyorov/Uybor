from rest_framework.fields import EmailField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PhoneNumberModelSerializer(Serializer):
    class Meta:
        phone_number = EmailField(help_text='Email address')


# class Advertisement