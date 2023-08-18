import datetime
from django.db import models
from django.contrib.auth.models import User

from books.models import Book
from mybooks.models import MyBook


class ShareBook(models.Model):
    """
    Model to track shared books
    """

    shelf_book = models.ForeignKey(
        MyBook, on_delete=models.CASCADE, help_text="Select a book to share"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, help_text="Select a book to share"
    )
    loaner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loaner")
    borrower = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="borrower",
        help_text="Select a user to share with",
    )
    borrower_alt = models.CharField(
        max_length=100, blank=True, help_text="Enter a name to share with a non-user"
    )
    date_shared = models.DateField(
        null=True, blank=True, help_text="Date shared. Leave blank to use today's date"
    )
    date_returned = models.DateField(
        null=True,
        blank=True,
        help_text="Date returned. Leave blank to use today's date",
    )
    returned = models.BooleanField(default=False)
    notes = models.TextField(
        max_length=280, blank=True, help_text="Enter any notes about the loan"
    )

    class Meta:
        ordering = ["-date_shared"]

    def __str__(self):
        return f"{self.shelf_book} shared with {self.borrower}"

    def save(self, *args, **kwargs):
        if self.borrower_alt:
            self.borrower = None
        if not self.date_shared:
            self.date_shared = datetime.date.today()
        if self.returned and not self.date_returned:
            self.date_returned = datetime.date.today()
        super().save(*args, **kwargs)


class ShareBookRequest(models.Model):
    """
    Model for shared book requests
    Users can request to borrow a book from another user
    """

    shelf_book = models.ForeignKey(
        MyBook, on_delete=models.CASCADE, help_text="Select a book to share"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, help_text="Select a book to share"
    )
    loaner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="loaner_request"
    )
    borrower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="borrower_request",
        help_text="Select a user to share with",
    )
    date_requested = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    reject_reason = models.TextField(
        max_length=280, blank=True, help_text="Enter a reason for rejecting the request"
    )

    class Meta:
        ordering = ["-date_requested"]

    def __str__(self):
        return f"{self.borrower} requested to borrow {self.shelf_book}"
