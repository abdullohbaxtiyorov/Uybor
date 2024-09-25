from django.contrib import admin
from django.contrib.admin import register, ModelAdmin

from apps.models import User, Advertisement


@register(User)
class UserAdmin(ModelAdmin):
    pass

@register(Advertisement)
class AdvertisementAdmin(ModelAdmin):
    pass