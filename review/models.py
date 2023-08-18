from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from books.models import Book


class MyBookReview(models.Model):
    """
    Model representing a book review.
    Fields to be displayed are user, book, review, rating, date_added.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, help_text="Select the book"
    )
    review = models.TextField(max_length=500, blank=True, help_text="Enter your review")
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Enter your rating",
    )
    private = models.BooleanField(
        default=True, help_text="Make review invisible to others"
    )
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        unique_together = ["user", "book"]

    def __str__(self):
        return self.book.title + " " + str(self.rating) + "/10"
