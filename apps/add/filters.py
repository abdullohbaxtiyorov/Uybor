from django_filters import rest_framework as filters
from django_filters import NumberFilter, ChoiceFilter, ModelChoiceFilter
from .models import Advertisement, Options


class OptionsFilter(filters.FilterSet):
    number_rooms = NumberFilter(field_name='number_rooms', label="Number of Rooms")
    apartment_area = NumberFilter(field_name='apartment_area', label="Apartment Area")
    floor = NumberFilter(field_name='floor', label="Floor")
    floors_building = NumberFilter(field_name='floors_building', label="Floors in Building")
    repair = filters.CharFilter(field_name='repair', lookup_expr='icontains', label="Repair")
    building_material = filters.CharFilter(field_name='building_material', lookup_expr='icontains',
                                           label="Building Material")
    land_area = NumberFilter(field_name='land_area', label="Land Area")
    house_area = NumberFilter(field_name='house_area', label="House Area")
    floors_house = NumberFilter(field_name='floors_house', label="Floors in House")
    office_area = NumberFilter(field_name='office_area', label="Office Area")

    class Meta:
        model = Options
        fields = [
            'number_rooms', 'apartment_area', 'floor', 'floors_building',
            'repair', 'building_material', 'land_area', 'house_area',
            'floors_house', 'office_area'
        ]


class AdvertisementFilter(filters.FilterSet):
    advertisement_type = ChoiceFilter(
        choices=Advertisement.AdvertisementTypeChoices.choices,
        label="Advertisement Type"
    )
    estate_type = ChoiceFilter(
        choices=Advertisement.EstateTypeChoices.choices,
        label="Estate Type"
    )
    options = ModelChoiceFilter(queryset=Options.objects.all(), field_name='options')

    class Meta:
        model = Advertisement
        fields = ['advertisement_type', 'estate_type', 'options']
