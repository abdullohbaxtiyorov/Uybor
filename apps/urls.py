from django.urls import path

from apps.views import UserListCreateAPIView

urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='user-list'),
]