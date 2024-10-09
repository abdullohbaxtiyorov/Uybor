from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from apps.add.views import AdvertisementListAPIView, \
    OptionsListCreateAPIView, MyAddsView

urlpatterns = [

    path('advertisement', AdvertisementListAPIView.as_view(), name='advertisements'),
    path('advertisement', OptionsListCreateAPIView.as_view(), name='options'),
    path('myadd/', MyAddsView.as_view(), name='options'),

    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
