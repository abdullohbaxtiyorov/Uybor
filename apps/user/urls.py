from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MyAddListApiView
from .views import RegisterUser, VerifyPhone, UserListCreateAPIView, MyProfileModelViewSet

router = DefaultRouter()
router.register(r'my-adds', MyAddListApiView, basename='my-adds')
router.register(r'my-profile', MyProfileModelViewSet, basename='my-profile')

urlpatterns = [
    path('', include(router.urls)),

    path('user', UserListCreateAPIView.as_view(), name='user-list'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('verify/', VerifyPhone.as_view(), name='verify'),

]

