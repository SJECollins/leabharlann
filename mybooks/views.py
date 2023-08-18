from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from shelf.utils import increment_book_shelf, increment_book_read
from books.models import Book
from review.models import MyBookReview
from mygenres.models import MyGenre
from myauthors.models import MyAuthor
from .models import MyBook
from .forms import (
    MyBookForm,
    MyBookEditForm,
    MyBookFinishedForm,
    MyBookNotesForm,
    MyBookProgressForm,
    MyBookStartForm,
    MyBookSummaryForm,
)


def my_books(request, pk):
    """
    View function for listing all books on the user's shelf.
    Includes search and filter functionality.
    """
    shelf_owner = User.objects.get(pk=pk)
    mybooks = MyBook.objects.filter(user=shelf_owner).order_by("book__title")
    mybooks_count = mybooks.count()

    query = None
    filter = None
    direction = None

    if request.GET:
        filterkey = request.GET.get("filterkey")
        if filterkey is None or filterkey == "default":
            mybooks = mybooks.order_by("book__title")
        else:
            filterkey = filterkey.split("_")[0]
            filter = filterkey
            if filterkey == "author":
                filterkey = "book__author__name"
            elif filterkey == "genre":
                filterkey = "book__genre__name"
            elif filterkey == "title":
                filterkey = "book__title"
            elif filterkey == "date":
                filterkey = "added_on"
            direction = request.GET.get("filterkey")
            direction = direction.split("_")[1]
            if direction == "desc":
                filterkey = f"-{filterkey}"
            mybooks = mybooks.order_by(filterkey)

        if "search" in request.GET:
            query = request.GET.get("search")
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse("mybooks:mybooks", args=[shelf_owner.id]))

            queries = (
                Q(book__title__icontains=query)
                | Q(book__author__name__icontains=query)
                | Q(book__genre__name__icontains=query)
            )
            mybooks = mybooks.filter(queries)

    current_filterkey = filter + "_" + direction if filter and direction else None
    paginator = Paginator(mybooks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "shelf_owner": shelf_owner,
        "page_obj": page_obj,
        "mybooks_count": mybooks_count,
        "current_filterkey": current_filterkey,
    }
    return render(request, "mybooks/mybook-list.html", context)


def mybook_detail(request, pk):
    """
    View function for displaying a single book.
    Returns the book object with the primary key (pk) equal to the pk argument.
    """
    mybook = MyBook.objects.get(pk=pk)
    myreview = MyBookReview.objects.filter(user=request.user, book=mybook.book).first()
    context = {"mybook": mybook, "myreview": myreview}
    return render(request, "mybooks/mybook.html", context)


def add_mybook(request, book_id=None):
    """
    View function for adding a book to the user's shelf.
    """
    if request.method == "POST":
        form = MyBookForm(request.POST, request.FILES)
        if form.is_valid():
            mybook = form.save(commit=False)
            mybook.user = request.user
            mybook.save()
            increment_book_shelf(mybook.id)
            if not MyAuthor.objects.filter(
                user=request.user, author=mybook.book.author
            ):
                new_myauthor = MyAuthor.objects.create(
                    user=request.user, author=mybook.book.author
                )
                new_myauthor.save()
            for new_genre in mybook.book.genre.all():
                if not MyGenre.objects.filter(user=request.user, genre=new_genre):
                    new_mygenre = MyGenre.objects.create(
                        user=request.user, genre=new_genre
                    )
                    new_mygenre.save()

            messages.success(request, "Book added to your shelf")
            return redirect("mybooks:mybook-detail", pk=mybook.pk)
        else:
            messages.error(request, "There was an error adding the book to your shelf")
    else:
        if book_id:
            book = Book.objects.get(pk=book_id)
            form = MyBookForm(initial={"book": book})
        else:
            form = MyBookForm()
    return render(request, "mybooks/mybook-form.html", {"form": form})


def edit_mybook(request, pk):
    """
    View function for editing a book on the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        form = MyBookEditForm(request.POST, instance=mybook)
        if form.is_valid():
            mybook = form.save(commit=False)
            mybook.user = request.user
            mybook.save()
            messages.success(request, "Book updated successfully")
            return redirect("mybooks:mybook-detail", pk=mybook.pk)
        else:
            messages.error(request, "There was an error updating the book")
    else:
        form = MyBookEditForm(instance=mybook)
    context = {
        "form": form,
        "object_name": mybook.book.title,
        "action_name": "Edit",
    }
    return render(request, "generic-form.html", context)


def start_reading(request, pk):
    """
    View function for marking a book as currently reading on the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        form = MyBookStartForm(request.POST, instance=mybook)
        if form.is_valid():
            book = form.save(commit=False)
            book.currently_reading = True
            book.unread = False
            if book.finished or book.abandoned:
                book.restarted = True
                book.abandoned = False
                book.finished = False
                book.finished_reading_on = None
            book.save()
            messages.success(request, "Book marked as currently reading")
            return HttpResponse(status=204)
        else:
            messages.error(
                request, "There was an error marking the book as currently reading"
            )
    form = MyBookStartForm(instance=mybook)
    context = {
        "form": form,
        "modal_title": f"Mark {mybook.book.title} as currently reading?",
        "button_label": "Start",
    }
    return render(request, "modal/modal-form.html", context)


def update_progress(request, pk):
    """
    View function for updating the progress of a book on the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        form = MyBookProgressForm(request.POST, instance=mybook)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            messages.success(request, "Book progress updated")
            return HttpResponse(status=204)
        else:
            messages.error(request, "There was an error updating the book progress")
    form = MyBookProgressForm(instance=mybook)
    context = {
        "form": form,
        "modal_title": f"Update progress for {mybook.book.title}",
        "button_label": "Update",
    }
    return render(request, "modal/modal-form.html", context)


def update_notes(request, pk):
    """
    View function for updating the notes of a book on the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        form = MyBookNotesForm(request.POST, instance=mybook)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            messages.success(request, "Book notes updated")
            return HttpResponse(status=204)
        else:
            messages.error(request, "There was an error updating the book notes")
    form = MyBookNotesForm(instance=mybook)
    context = {
        "form": form,
        "modal_title": f"Update notes for {mybook.book.title}",
        "button_label": "Update",
    }
    return render(request, "modal/modal-form.html", context)


def update_summary(request, pk):
    """
    View function for updating the summary of a book on the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        form = MyBookSummaryForm(request.POST, instance=mybook)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            messages.success(request, "Book summary updated")
            return HttpResponse(status=204)
        else:
            messages.error(request, "There was an error updating the book summary")
    form = MyBookSummaryForm(instance=mybook)
    context = {
        "form": form,
        "modal_title": f"Update summary for {mybook.book.title}",
        "button_label": "Update",
    }
    return render(request, "modal/modal-form.html", context)


def mark_finished(request, pk):
    """
    View function for marking a book as finished on the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        form = MyBookFinishedForm(request.POST, instance=mybook)
        if form.is_valid():
            mybook = form.save(commit=False)
            increment_book_read(pk)
            mybook.save()
            messages.success(request, "Book marked as finished")
            return HttpResponse(status=204)
        else:
            messages.error(request, "There was an error marking the book as finished")
    form = MyBookFinishedForm(instance=mybook)
    context = {
        "form": form,
        "modal_title": f"Mark {mybook.book.title} as finished?",
        "button_label": "Finish",
    }
    return render(request, "modal/modal-form.html", context)


def mark_abandoned(request, pk):
    """
    View function for marking a book as abandoned on the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        mybook.abandoned = True
        if mybook.number_of_times_read == 0:
            mybook.unread = True
        mybook.currently_reading = False
        mybook.save()
        messages.success(request, "Book marked as abandoned")
        return HttpResponse(status=204)
    context = {
        "modal_title": f"Mark {mybook.book.title} as abandoned?",
        "modal_message": f"Are you sure you want to mark {mybook.book.title} as abandoned?",
        "button_label": "Abandon",
    }
    return render(request, "modal/modal-form.html", context)


def toggle_favourite(request, pk):
    """
    View function for toggling a book's favourite status on the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    mybook.favourite = not mybook.favourite
    mybook.save()
    messages.success(request, "Book favourite status updated")
    return redirect("mybooks:mybook-detail", pk=mybook.pk)


def toggle_private(request, pk):
    """
    View function for toggling a book's private status on the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    mybook.private = not mybook.private
    mybook.save()
    messages.success(request, "Book private status updated")
    return redirect("mybooks:mybook-detail", pk=mybook.pk)


def delete_mybook(request, pk):
    """
    View function for deleting a book from the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        mybook.book.number_shelves -= 1
        mybook.delete()
        messages.success(request, "The book has been deleted from your shelf")
        return redirect("mybooks:mybooks", pk=request.user.pk)
    context = {
        "object": mybook,
        "object_name": mybook.book.title,
    }
    return render(request, "delete-form.html", context)
