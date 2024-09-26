from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import User, Advertisement, Image, Options


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ImageModelSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', ]


class PhoneNumberModelSerializer(Serializer):
    class Meta:
        phone_number = CharField(max_length=11)


class OptionModelSerializer(ModelSerializer):
    class Meta:
        model = Options
        fields = '__all__'


class AdvertisementModelSerializer(ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
        extra_kwargs = {
            'facilities': {'write_only': True},
        }




class PhoneNumberSerializer(Serializer):
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
