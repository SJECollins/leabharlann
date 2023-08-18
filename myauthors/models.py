from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from books.models import Author


class MyAuthor(models.Model):
    """
    Model representing an author that the user has read.
    Fields to be displayed are author, user, notes, favourite.
    """

    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, help_text="Select the author"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(
        max_length=500,
        blank=True,
        help_text="Enter any notes you have about this author",
    )
    number_of_books_read = models.PositiveIntegerField(default=0)
    favourite = models.BooleanField(
        default=False, help_text="Is this one of your favourite authors?"
    )

    def __str__(self):
        return self.author.name

    def get_absolute_url(self):
        return reverse("myauthor-detail", args=[str(self.id)])
