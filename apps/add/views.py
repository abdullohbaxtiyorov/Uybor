from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.add.filters import AdvertisementFilter
from apps.add.models import Advertisement, Options
from apps.add.pagination import LargeResultsSetPagination
from apps.add.serializers import AdvertisementModelSerializer, \
    OptionModelSerializer


@extend_schema(
    request={
        'multipart/form-data': AdvertisementModelSerializer,
    },
    responses={201: AdvertisementModelSerializer},
    tags=['Advertisement']
)
class AdvertisementListAPIView(ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementModelSerializer
    pagination_class = LargeResultsSetPagination
    parser_classes = [MultiPartParser, JSONParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter


# @extend_schema(tags=['Advertisement'])
class OptionsListCreateAPIView(ListCreateAPIView):
    queryset = Options.objects.all()
    serializer_class = (OptionModelSerializer)


class MyAddsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        adds = Advertisement.objects.filter(owner=request.user)
