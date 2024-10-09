from rest_framework.fields import ListField, ImageField
from rest_framework.serializers import ModelSerializer

from apps.add.models import Advertisement, Image, Options
from apps.user.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class OptionModelSerializer(ModelSerializer):
    class Meta:
        model = Options
        fields = '__all__'


class ImageModelSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class AdvertisementModelSerializer(ModelSerializer):
    options = OptionModelSerializer(write_only=True)
    images = ListField(
        child=ImageField(),
        write_only=True
    )

    class Meta:
        model = Advertisement
        fields = '__all__'

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        images_data = validated_data.pop('images')
        advertisement = Advertisement.objects.create(**validated_data)
        options_instance = Options.objects.create(advertisement=advertisement, **options_data)
        for image_data in images_data:
            Image.objects.create(advertisement=advertisement, image=image_data)
        return advertisement

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['images'] = ImageModelSerializer(instance.images.all(), many=True).data
        repr['options'] = OptionModelSerializer(instance.options).data
        return repr
# asddassdasdasdsd