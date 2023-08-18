from django.contrib import admin
from .models import MyBookReview


@admin.register(MyBookReview)
class MyBookReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "rating", "date_added")
    list_filter = ("user", "book", "rating", "date_added")
    search_fields = ("user", "book", "rating", "date_added")
