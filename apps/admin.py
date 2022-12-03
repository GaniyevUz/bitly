from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.models import Url, User


@admin.register(Url)
class UrlAdmin(ModelAdmin):
    list_display = ('short_name', 'long_name', 'clicked_count')
    exclude = ('clicked_count',)


@admin.register(User)
class User(ModelAdmin):
    pass
