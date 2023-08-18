from django.shortcuts import get_object_or_404
from books.models import Book, Author, Genre
from mybooks.models import MyBook
from myauthors.models import MyAuthor
from mygenres.models import MyGenre


def increment_book_read(pk):
    """
    Increment the number of times a book has been read.
    """
    mybook = get_object_or_404(MyBook, pk=pk)
    if not mybook.finished:
        mybook.finished = True
    mybook.number_of_times_read += 1

    book = Book.objects.filter(id=mybook.book.id).first()
    if book:
        book.number_reads += 1
        book.save()

    myauthor = MyAuthor.objects.filter(
        user=mybook.user, author=mybook.book.author
    ).first()
    # Update number of books read by author if finished
    if myauthor:
        myauthor.number_of_books_read = mybook.number_of_times_read
        myauthor.save()

    author = Author.objects.filter(id=mybook.book.author.id).first()
    # Update number of books read by author if finished
    if author:
        author.number_reads += 1
        author.save()

    mygenres = MyGenre.objects.filter(
        user=mybook.user, genre__in=mybook.book.genre.all()
    )
    # Update number of books read by genre if finished
    for mygenre in mygenres:
        mygenre.number_of_books_read = mybook.number_of_times_read
        mygenre.save()

    genres = Genre.objects.filter(id__in=mybook.book.genre.all())
    # Update number of books read by genre if finished
    for genre in genres:
        genre.number_reads += 1
        genre.save()

    return mybook


def increment_book_shelf(pk):
    """
    Increment the number of times a book has been added to a shelf.
    """
    mybook = get_object_or_404(MyBook, pk=pk)

    book = Book.objects.filter(id=mybook.book.id).first()
    if book:
        book.number_shelves += 1
        book.save()

    author = Author.objects.filter(id=mybook.book.author.id).first()
    # Update number of books shelved by author
    if author:
        author.number_shelves += 1
        author.save()

    genres = Genre.objects.filter(id__in=mybook.book.genre.all())
    # Update number of books shelved by genre
    for genre in genres:
        genre.number_shelves += 1
        genre.save()
