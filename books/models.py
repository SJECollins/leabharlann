from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from leabharlann.utils import edit_image


class Author(models.Model):
    """
    Model representing an author.
    Fields to be displayed are name.
    """

    honorific = models.CharField(
        max_length=10,
        blank=True,
        help_text="Enter the author's honorific (e.g. Mr, Mrs, Ms, Dr, etc.)",
    )
    first_name = models.CharField(
        max_length=100, blank=True, help_text="Enter the author's first name"
    )
    middle_name = models.CharField(
        max_length=100, blank=True, help_text="Enter the author's middle name"
    )
    last_name = models.CharField(
        max_length=100, blank=True, help_text="Enter the author's last name"
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Enter the author's name as it should be displayed",
    )
    created_on = models.DateTimeField(auto_now_add=True)
    number_shelves = models.PositiveIntegerField(default=0)
    number_reads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        """
        Override the save method of the Author model to create the name field.
        """
        self.name = (
            self.honorific
            + " "
            + self.first_name
            + " "
            + self.middle_name
            + " "
            + self.last_name
        )
        super().save(*args, **kwargs)


class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science-Fiction, Fantasy, etc.).
    Fields to be displayed are name.
    """

    name = models.CharField(
        max_length=100,
        help_text="Enter a book genre (e.g. Science Fiction, Fantasy, etc.)",
    )
    number_shelves = models.PositiveIntegerField(default=0)
    number_reads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre-detail", args=[str(self.id)])


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    Fields to be displayed are title, author, genre, book_cover.
    """

    title = models.CharField(max_length=140, help_text="Enter the book's title")
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, help_text="Select the book's author"
    )
    genre = models.ManyToManyField(
        Genre, help_text="Select at least one genre for this book"
    )
    book_cover = models.ImageField(
        upload_to="book_covers",
        blank=True,
        help_text="Optional. Upload a book cover image",
    )
    number_shelves = models.PositiveIntegerField(default=0)
    number_reads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title + " by " + self.author.name

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    def save(self, *args, **kwargs):
        """
        Override the save method of the Book model to resize the book cover.
        """
        if self.book_cover:
            new_image = edit_image(self.book_cover, 300, 300)
            self.book_cover = new_image
        super().save(*args, **kwargs)
