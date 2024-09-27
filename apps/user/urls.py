from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MyAddListApiView
from .views import RegisterUser, VerifyPhone, UserListCreateAPIView, MyProfileModelViewSet

router = DefaultRouter()
router.register(r'myadds', MyAddListApiView)
router.register(r'myprofile', MyProfileModelViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('user', UserListCreateAPIView.as_view(), name='user-list'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('verify/', VerifyPhone.as_view(), name='verify'),

]
