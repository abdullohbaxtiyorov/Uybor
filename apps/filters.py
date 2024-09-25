from unittest.mock import PropertyMock

from django_filters import FilterSet, ChoiceFilter

from apps.models import Advertisement


class AdvertisementTypeFilter(FilterSet):
        property_type = ChoiceFilter(
            field_name='property_type',
            choices = Advertisement.AdvertisementTypeChoices
        )



