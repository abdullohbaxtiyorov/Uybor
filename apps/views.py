from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView
from tutorial.quickstart.serializers import UserSerializer
from apps.models import User
@extend_schema(tags=['Users'])
class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



# @extend_schema(tags=['Login-register'])
# class