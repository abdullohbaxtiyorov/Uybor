from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField, ImageField, BooleanField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    class UserChoices(TextChoices):
        PRIVATE_OWNER = 'private_owner', _('Private Owner')
        ADMIN = 'admin', _('Admin')
        REALTOR = 'realtor', _('Realtor')
        DEVELOPER = 'developer', _('Developer')

    # Validators can be adjusted according to your requirements
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                     message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed.")

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, validators=[phone_validator])
    user_type = models.CharField(choices=UserChoices.choices, max_length=20, default=UserChoices.PRIVATE_OWNER)
    photo = models.ImageField(upload_to='photos/users', blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
    )
    password = CharField(_("password"), max_length=128, null=True)

    def __str__(self):
        return self.phone_number
