from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import CharField, TextChoices, ImageField, Model, ForeignKey, CASCADE, JSONField, DecimalField, \
    SmallIntegerField


class User(Model):
    class UserChoices(TextChoices):
        PRIVATE_OWNER = 'private_owner', 'Private_Owner'
        ADMIN = 'admin', 'Admin'
        REALTOR = 'realtor', 'Realtor'
        DEVELOPER = 'developer', 'Developer'

    first_name = CharField(max_length=255, blank=True, null=True)
    last_name = CharField(max_length=255, blank=True, null=True)
    phone_number = CharField(max_length=20, unique=True)
    user_type = CharField(choices=UserChoices.choices, max_length=20, default=UserChoices.PRIVATE_OWNER)
    photo = ImageField(upload_to='photos/users', blank=True, null=True)


class Advertisement(Model):
    class AdvertisementTypeChoices(TextChoices):
        SELL = 'sell', 'Sell'
        RENT = 'rent', 'Rent'

    class EstateTypeChoices(TextChoices):
        APARTMENT = 'apartment', 'Apartment'
        HOUSE = 'house', 'House'
        FOR_BUSINESS = 'business', 'Business'
        LAND = 'land', 'Land'

    advertisement = CharField(max_length=25, choices=AdvertisementTypeChoices.choices)
    estate_type = CharField(max_length=25, choices=EstateTypeChoices.choices)
    description = CharField(max_length=255, blank=True, null=True)
    # phone_number = CharField(max_length=20, default=User.phone_number)
    phone_number = CharField(max_length=20, unique=True)
    facilities = JSONField(blank=True, null=True)


class Image(Model):
    advertisement = ForeignKey('apps.Advertisement', on_delete=CASCADE, related_name='images')
    image = ImageField(upload_to='images',
                       validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])


class Options(Model):
    advertisement = ForeignKey('apps.Advertisement', on_delete=CASCADE, related_name='options')
    number_rooms = SmallIntegerField(default=0,null=True,blank=True)
    apartment_area = SmallIntegerField(blank=True, null=True)
    floor = SmallIntegerField(null=True, blank=True)
    floors_building = SmallIntegerField(null=True, blank=True)
    repair = CharField(max_length=255, blank=True, null=True)
    building_material = CharField(max_length=255, blank=True, null=True)
    land_area = SmallIntegerField(null=True, blank=True)
    house_area = SmallIntegerField(null=True, blank=True)
    floors_house = SmallIntegerField(null=True, blank=True)
    office_area = SmallIntegerField(null=True, blank=True)



# class Price(Model):
#     class PriceChoices(TextChoices):
#         YEVRO = 'yevro', 'Yevro'
#         SOM = 'som', 'Som'
#
#     advertisement_id = ForeignKey('apps.Advertisement', CASCADE, related_name='prices')
#     price = DecimalField(max_digits=10, decimal_places=2)
#     price_type = CharField(max_length=25, choices=PriceChoices.choices)


class SiteSettings(Model):
    pass