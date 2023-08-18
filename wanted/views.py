from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


from books.models import Book
from .models import Wanted
from .forms import WantedForm


def wanted(request, pk=None):
    """
    View function for listing all wanted books on the user's shelf.
    """
    shelf_owner = User.objects.get(pk=pk)
    wanted = Wanted.objects.filter(user=shelf_owner).order_by("-added_on")
    wanted_count = wanted.count()
    context = {
        "shelf_owner": shelf_owner,
        "wanted": wanted,
        "wanted_count": wanted_count,
    }
    return render(request, "wanted/wanted.html", context)


def add_wanted(request, book_id=None):
    """
    View function for adding a wanted book to the user's shelf.
    """
    if request.method == "POST":
        form = WantedForm(request.POST)
        if form.is_valid():
            wanted = form.save(commit=False)
            wanted.user = request.user
            wanted.save()
            messages.success(request, "Book added to your wanted list")
            return redirect("wanted:wanted", pk=request.user.pk)
        else:
            messages.error(
                request, "There was an error adding the book to your wanted list"
            )
    else:
        if book_id:
            book = Book.objects.get(pk=book_id)
            form = WantedForm(initial={"book": book})
        else:
            form = WantedForm()
    context = {
        "form": form,
        "object_name": "Wanted Book",
    }
    return render(request, "wanted/wanted-form.html", context)


def edit_wanted(request, pk):
    """
    View function for editing a wanted book on the user's shelf.
    """
    wanted = Wanted.objects.get(pk=pk)
    if request.method == "POST":
        form = WantedForm(request.POST, instance=wanted)
        if form.is_valid():
            wanted = form.save(commit=False)
            wanted.user = request.user
            wanted.save()
            messages.success(request, "Book updated successfully")
            return redirect("wanted:wanted", pk=request.user.pk)
        else:
            messages.error(request, "There was an error updating the book")
    else:
        form = WantedForm(instance=wanted)
    context = {"form": form, "object_name": wanted.book.title, "action_name": "Edit"}
    return render(request, "generic-form.html", context)


def delete_wanted(request, pk):
    """
    View function for deleting a wanted book from the user's shelf.
    """
    wanted = Wanted.objects.get(pk=pk)
    if request.method == "POST":
        wanted.delete()
        messages.success(request, "The book has been deleted from your wanted list")
        return redirect("wanted:wanted", pk=request.user.pk)
    context = {
        "object": wanted,
        "object_name": wanted.book.title,
    }
    return render(request, "delete-form.html", context)
