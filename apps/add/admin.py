from django.contrib.admin import register, ModelAdmin

from apps.add.models import Advertisement
from apps.user.models import User

@register(User)
class UserAdmin(ModelAdmin):
    pass

@register(Advertisement)
class AdvertisementAdmin(ModelAdmin):
    pass