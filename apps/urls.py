from django.urls import path

from apps.views import UserListCreateAPIView, AdvertisementListCreateAPIView, SendCodeAPIView, VerifyCodeAPIView, \
    OptionsListCreateAPIView, ImageCreateAPIView

urlpatterns = [

    path('user', UserListCreateAPIView.as_view(), name='user-list'),
    path('advertisement', AdvertisementListCreateAPIView.as_view(), name='advertisements'),
    path('advertisement', OptionsListCreateAPIView.as_view(), name='options'),
    path('image', ImageCreateAPIView.as_view(), name='image'),
    path('send_code', SendCodeAPIView.as_view(),name ='send_code'),
    path('verify_code', VerifyCodeAPIView.as_view(),name ='verify_code')
]