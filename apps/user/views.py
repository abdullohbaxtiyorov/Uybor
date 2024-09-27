import random

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from twilio.rest import Client

from apps.add.serializers import UserModelSerializer, AdvertisementModelSerializer
from apps.user.serializer import RegisterUserSerializer
from .models import User
from .serializer import UserSerializer
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

        # Check if the phone number already exists
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'Phone number is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a 6-digit verification code
        verification_code = random.randint(100000, 999999)

        # Save the code in session (or another preferred way)
        request.session['verification_code'] = verification_code

        # Send the SMS via Twilio
        message = client.messages.create(
            body=f'Your verification code is {verification_code}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        # Serialize the user data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created. Verification code sent.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Send_code"])
class VerifyPhone(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')

        # Get the code from session (or database)
        correct_code = request.session.get('verification_code')

        if str(verification_code) == str(correct_code):
            try:
                user = User.objects.get(phone_number=phone_number)
                user.is_phone_verified = True
                user.save()
                return Response({'message': 'Phone number verified successfully.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['my_add'])
class MyAddListApiView(ListAPIView):
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