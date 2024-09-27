from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField, ImageField, BooleanField


class User(AbstractUser):
    class UserChoices(TextChoices):
        PRIVATE_OWNER = 'private_owner', 'Private Owner'
        ADMIN = 'admin', 'Admin'
        REALTOR = 'realtor', 'Realtor'
        DEVELOPER = 'developer', 'Developer'

    first_name = CharField(max_length=255, blank=True, null=True)
    last_name = CharField(max_length=255, blank=True, null=True)
    phone_number = CharField(max_length=20, unique=True)
    user_type = CharField(choices=UserChoices.choices, max_length=20, default=UserChoices.PRIVATE_OWNER)
    photo = ImageField(upload_to='photos/users', blank=True, null=True)
    is_phone_verified = BooleanField(default=False)

    def __str__(self):
        return self.phone_number

