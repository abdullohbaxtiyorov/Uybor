from django.contrib import admin
from django.contrib.admin import register, ModelAdmin

from apps.models import User


@register(User)
class UserAdmin(ModelAdmin):
    pass