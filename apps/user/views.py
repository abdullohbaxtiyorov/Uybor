import random

from django.conf import settings
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from twilio.rest import Client

from apps.add.serializers import UserModelSerializer, AdvertisementModelSerializer
from .models import User  # Make sure to import your User model
from .serializers import RegisterUserSerializer
from .serializers import VerifySerializer  # Import your serializer
from ..add.models import Advertisement

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
        # Check if the phone number already exists
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({
                'error': 'Phone number is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

            # Save the code in session (or another preferred way)
            request.session['verification_code'] = verification_code

            # Instead of sending SMS, return the code in the response
        return Response({'message': 'User created. Verification code:', 'verification_code': verification_code},
                        status=status.HTTP_201_CREATED)

@extend_schema(tags=["Send_code"])
class VerifyPhone(APIView):
    serializer_class = VerifySerializer

    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('code')

        # Get the code from session
        correct_code = request.session.get('verification_code')

        if str(verification_code) == str(correct_code):
            # Check if the user exists
            user, created = User.objects.get_or_create(phone_number=phone_number)

            # If user is newly created, you might want to set additional fields
            if created:
                user.is_phone_verified = True
                user.save()

            # Authenticate the user by logging them in
            login(request, user)  # Log the user in

            return Response({'message': 'Phone number verified and user authenticated successfully.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['my_add'])
class MyAddListApiView(ModelViewSet):
    serializer_class = AdvertisementModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Advertisement.objects.filter(user=self.request.owner)

@extend_schema(tags=['MyProfile'])
class MyProfileModelViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
