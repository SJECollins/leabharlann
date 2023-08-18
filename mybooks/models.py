from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

from myauthors.models import MyAuthor
from mygenres.models import MyGenre
from books.models import Book, Author, Genre


class MyBook(models.Model):
    """
    Model representing a specific copy of a book (i.e. a book on the user's "shelf").
    Fields to be displayed are user, book, summary, started_reading_on, currently_reading, abandoned, finished_reading_on, finished, favourite, notes.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, help_text="Select the book"
    )
    summary = models.TextField(
        max_length=500, blank=True, help_text="Enter a brief description of the book"
    )
    unread = models.BooleanField(default=True, help_text="Have you read this book?")
    started_reading_on = models.DateField(
        blank=True, null=True, help_text="When did you start reading this book?"
    )
    currently_reading = models.BooleanField(
        default=False, help_text="Are you currently reading this book?"
    )
    abandoned = models.BooleanField(
        default=False,
        help_text="Have you abandoned this book? If so, maybe leave a note as to why.",
    )
    finished_reading_on = models.DateField(
        blank=True,
        null=True,
        help_text="When did you finish reading this book? If blank, today's date will be used.",
    )
    finished = models.BooleanField(
        default=False, help_text="Have you finished reading this book?"
    )
    restarted = models.BooleanField(
        default=False, help_text="Have you restarted reading this book?"
    )
    favourite = models.BooleanField(
        default=False, help_text="Is this one of your favourite books?"
    )
    notes = models.TextField(
        max_length=500, blank=True, help_text="Enter any notes you have about this book"
    )
    private = models.BooleanField(
        default=False, help_text="Book won't be visible to others on your shelf"
    )
    pages_total = models.PositiveIntegerField(
        default=0, help_text="How many pages are there in total?"
    )
    pages_read = models.PositiveIntegerField(
        default=0, help_text="How many pages have you read?"
    )
    number_of_times_read = models.PositiveIntegerField(
        default=0, help_text="How many times have you read this book?"
    )
    percentage_read = models.PositiveIntegerField(default=0)
    added_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.book.title

    def get_absolute_url(self):
        return reverse("mybook-detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        # Set currently reading if started reading and not finished or abandoned
        if self.started_reading_on and not self.finished and not self.abandoned:
            self.currently_reading = True
            self.unread = False
        # Set not currently reading if finished or abandoned
        if self.currently_reading and self.finished and not self.restarted:
            self.currently_reading = False
        if self.currently_reading and self.abandoned and not self.restarted:
            self.currently_reading = False
        if self.abandoned and self.restarted:
            self.abandoned = False
        if self.finished and not self.restarted:
            # Set finished reading date if not set
            if self.finished_reading_on is None:
                self.finished_reading_on = datetime.date.today()
            # Set not currently reading if finished
            if self.currently_reading:
                self.currently_reading = False

            myauthor = MyAuthor.objects.filter(
                user=self.user, author=self.book.author
            ).first()
            # Update number of books read by author if finished
            if myauthor:
                myauthor.number_of_books_read = self.number_of_times_read
                myauthor.save()

            author = Author.objects.filter(id=self.book.author.id).first()
            # Update number of books read by author if finished
            if author:
                author.number_reads += 1
                author.save()

            mygenres = MyGenre.objects.filter(
                user=self.user, genre__in=self.book.genre.all()
            )
            # Update number of books read by genre if finished
            for mygenre in mygenres:
                mygenre.number_of_books_read = self.number_of_times_read
                mygenre.save()

            genres = Genre.objects.filter(id__in=self.book.genre.all())
            # Update number of books read by genre if finished
            for genre in genres:
                genre.number_reads += 1
                genre.save()

        # Update percentage read
        if self.pages_total > 0:
            self.percentage_read = round((self.pages_read / self.pages_total) * 100)

        # Call the superclass's save method to save the model without recursion
        super(MyBook, self).save(*args, **kwargs)
