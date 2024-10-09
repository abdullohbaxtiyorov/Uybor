from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import CharField, TextChoices, ImageField, Model, ForeignKey, CASCADE, JSONField, \
    SmallIntegerField, ManyToManyField


class Advertisement(Model):
    class AdvertisementTypeChoices(TextChoices):
        SELL = 'sell', 'Sell'
        RENT = 'rent', 'Rent'

    class EstateTypeChoices(TextChoices):
        APARTMENT = 'apartment', 'Apartment'
        HOUSE = 'house', 'House'
        FOR_BUSINESS = 'business', 'Business'
        LAND = 'land', 'Land'

    advertisement_type = CharField(max_length=25, choices=AdvertisementTypeChoices.choices)
    estate_type = CharField(max_length=25, choices=EstateTypeChoices.choices)
    description = CharField(max_length=255, blank=True, null=True)
    phone_number = SmallIntegerField()
    facilities = JSONField(blank=True, null=True)
    images = ManyToManyField('Image', related_name='advertisements', blank=True)
    options = ForeignKey('Options', CASCADE, related_name='advertisements')
    user = ForeignKey('user.User', CASCADE)


class Options(Model):
    number_rooms = SmallIntegerField(default=0, null=True, blank=True)
    apartment_area = SmallIntegerField(blank=True, null=True)
    floor = SmallIntegerField(null=True, blank=True)
    floors_building = SmallIntegerField(null=True, blank=True)
    repair = CharField(max_length=255, blank=True, null=True)
    building_material = CharField(max_length=255, blank=True, null=True)
    land_area = SmallIntegerField(null=True, blank=True)
    house_area = SmallIntegerField(null=True, blank=True)
    floors_house = SmallIntegerField(null=True, blank=True)
    office_area = SmallIntegerField(null=True, blank=True)





class Image(Model):
    image = ImageField(upload_to='images',
                       validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])


