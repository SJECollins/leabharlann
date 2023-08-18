from django.contrib import admin
from .models import MyBook


@admin.register(MyBook)
class MyBookAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "currently_reading", "finished")
    list_filter = ("user", "book", "currently_reading", "finished")
    search_fields = ("user", "book", "currently_reading", "finished")
