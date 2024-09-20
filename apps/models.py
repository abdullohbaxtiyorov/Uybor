from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import CharField, TextChoices, ImageField, Model, ForeignKey, CASCADE, JSONField


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

    class EstateTypechoices(TextChoices):
        APARTMENT = 'apartment', 'Apartment'
        HOUSE = 'house', 'House'
        FOR_BUSINESS = 'business', 'Business'
        LAND = 'land', 'Land'

    advertisement = CharField(max_length=25, choices=AdvertisementTypeChoices.choices)
    estate_type = CharField(max_length=25, choices=EstateTypechoices.choices)
    description = CharField(max_length=255, blank=True, null=True)
    phone_number = CharField(max_length=20, default=User.phone_number)
    facilities = JSONField(blank=True, null=True)


class Image(Model):
    ad_id = ForeignKey('apps.Advertisement', CASCADE, related_name='images')
    image = ImageField(upload_to='images',
                       validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])