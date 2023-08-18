from django.contrib import admin
from .models import MyAuthor


@admin.register(MyAuthor)
class MyAuthorAdmin(admin.ModelAdmin):
    list_display = ("user", "author", "favourite")
    list_filter = ("user", "author", "favourite")
    search_fields = ("user", "author", "favourite")
