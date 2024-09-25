from random import randint
from django.core.cache import cache
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tutorial.quickstart.serializers import UserSerializer
from apps.models import User, Advertisement, Image
from apps.serializers import AdvertisementModelSerializer, PhoneNumberSerializer, VerifySerializer, ImageModelSerializer


@extend_schema(tags=['Users'])
class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



@extend_schema(tags=['Advertisement'])
class AdvertisementListCreateAPIView(ListCreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementModelSerializer


@extend_schema(tags=['Advertisement'])
class ImageListCreateAPIView(ListCreateAPIView):
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
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "OK"})
