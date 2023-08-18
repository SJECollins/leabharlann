from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from books.models import Book


class Wanted(models.Model):
    """
    Model representing a book that the user wants to read.
    Fields to be displayed are user, book, notes.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, help_text="Select the book"
    )
    notes = models.TextField(
        max_length=500, blank=True, help_text="Enter any notes you have about this book"
    )
    private = models.BooleanField(
        default=True, help_text="Book won't be visible to others"
    )
    added_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.book.title

    def get_absolute_url(self):
        return reverse("wanted-detail", args=[str(self.id)])
