from django.contrib import admin
from .models import MyGenre


@admin.register(MyGenre)
class MyGenreAdmin(admin.ModelAdmin):
    list_display = ("user", "genre", "favourite")
    list_filter = ("user", "genre", "favourite")
    search_fields = ("user", "genre", "favourite")
