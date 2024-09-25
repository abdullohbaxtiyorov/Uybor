from django.urls import path

from apps.views import UserListCreateAPIView, AdvertisementListCreateAPIView, SendCodeAPIView, VerifyCodeAPIView

urlpatterns = [

    path('user', UserListCreateAPIView.as_view(), name='user-list'),
    path('advertisement', AdvertisementListCreateAPIView.as_view(), name='advertisements'),
    path('advertisement', AdvertisementListCreateAPIView.as_view(), name='advertisements'),
    path('send_code', SendCodeAPIView.as_view(),name ='send_code'),
    path('verify_code', VerifyCodeAPIView.as_view(),name ='verify_code')
]