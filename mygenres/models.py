from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from books.models import Genre


# Create your models here.
class MyGenre(models.Model):
    """
    Model representing a genre that the user has read.
    Fields to be displayed are genre, user, notes, favourite.
    """

    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, help_text="Select the genre"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(
        max_length=500,
        blank=True,
        help_text="Enter any notes you have about this genre",
    )
    number_of_books_read = models.PositiveIntegerField(default=0)
    favourite = models.BooleanField(
        default=False, help_text="Is this one of your favourite genres?"
    )

    def __str__(self):
        return self.genre.name

    def get_absolute_url(self):
        return reverse("mygenre-detail", args=[str(self.id)])
