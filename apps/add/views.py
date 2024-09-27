from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from apps.add.models import Advertisement, Options
from apps.add.serializers import AdvertisementModelSerializer, \
    OptionModelSerializer


@extend_schema(
    request={
        'multipart/form-data': AdvertisementModelSerializer,
    },
    responses={201: AdvertisementModelSerializer},
    tags=['Advertisement']
)
class AdvertisementListCreateAPIView(CreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementModelSerializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Advertisement'])
class OptionsListCreateAPIView(ListCreateAPIView):
    queryset = Options.objects.all()
    serializer_class = OptionModelSerializer





