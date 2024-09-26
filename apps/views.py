from random import randint

from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, GenericAPIView, CreateAPIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.models import User, Advertisement, Image, Options
from apps.serializers import AdvertisementModelSerializer, PhoneNumberSerializer, VerifySerializer, \
    ImageModelSerializer, UserModelSerializer, OptionModelSerializer


@extend_schema(tags=['Users'])
class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


@extend_schema(tags=['Advertisement'])
class AdvertisementListCreateAPIView(CreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementModelSerializer
    parser_classes = [JSONParser]
    print(serializer_class.data)


@extend_schema(tags=['Advertisement'])
class OptionsListCreateAPIView(ListCreateAPIView):
    queryset = Options.objects.all()
    serializer_class = OptionModelSerializer


@extend_schema(tags=['Advertisement'])
class ImageCreateAPIView(CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageModelSerializer



@extend_schema(tags=["Send_code"])
class SendCodeAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = randint(100000, 999999)
        cache.set(phone_number, code, timeout=300)
        print(f"Phone: {phone_number}  Code: {code}")
        return Response({"message": f"{code}"})

    def get_queryset(self):
        return self.request.user


@extend_schema(tags=["Send_code"])
class VerifyCodeAPIView(GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "OK"})

