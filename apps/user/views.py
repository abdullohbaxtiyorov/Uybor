import random

from django.conf import settings
from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from twilio.rest import Client

from apps.add.serializers import UserModelSerializer, AdvertisementModelSerializer
from .models import User
from .serializers import RegisterUserSerializer
from .serializers import VerifySerializer
from ..add.models import Advertisement
from rest_framework_simplejwt.tokens import RefreshToken


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)





@extend_schema(tags=['Users'])
class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


@extend_schema(tags=["Send_code"])
class RegisterUser(APIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification_code = random.randint(100000, 999999)
        user, created = User.objects.get_or_create(phone_number=phone_number)
        cache.set(user.phone_number, verification_code, 120)
        return Response({"verification_code": verification_code})



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
@extend_schema(tags=["Send_code"])
class VerifyPhone(APIView):
    serializer_class = VerifySerializer

    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('code')

        cache_code = str(cache.get(phone_number))
        if str(verification_code) == cache_code:
            try:
                user = User.objects.get(phone_number=phone_number)

                tokens = get_tokens_for_user(user)

                return Response({
                    'message': 'Phone number verified and user authenticated successfully.',
                    'tokens': tokens
                }, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['MyAdd'])
class MyAddListApiView(ModelViewSet):
    serializer_class = AdvertisementModelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Advertisement.objects.none()
        return Advertisement.objects.filter(user=self.request.user)


@extend_schema(tags=['MyProfile'])
class MyProfileModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Foydalanuvchining o'zini olish
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        # Foydalanuvchining o'z profilini olish
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

# @extend_schema(tags=['MyProfile'])
# class MyProfileModelViewSet(ModelViewSet):
#     serializer_class = UserModelSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
