from django.urls import path, include

urlpatterns = [
    path('', include('apps.add.urls')),
    path('', include('apps.user.urls')),
]