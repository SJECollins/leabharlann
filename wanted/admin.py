from django.contrib import admin
from .models import Wanted


@admin.register(Wanted)
class WantedAdmin(admin.ModelAdmin):
    list_display = ("user", "book")
    list_filter = ("user", "book")
    search_fields = ("user", "book")
