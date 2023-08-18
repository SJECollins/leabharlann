from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from books.models import Author

from mybooks.models import MyBook
from .models import MyAuthor
from .forms import MyAuthorForm


# Create your views here.
def my_authors(request, pk=None):
    """
    View function for listing all authors on the user's shelf.
    """
    shelf_owner = User.objects.get(pk=pk)
    myauthors = MyAuthor.objects.filter(user=shelf_owner).order_by("author__name")
    myauthors_count = myauthors.count()

    query = None
    filter = None
    direction = None

    if request.GET:
        filterkey = request.GET.get("filterkey")
        if filterkey is None or filterkey == "default":
            myauthors = myauthors.order_by("author__name")
        else:
            filterkey = filterkey.split("_")[0]
            filter = filterkey
            if filterkey == "first":
                filterkey = "author__first_name"
            elif filterkey == "last":
                filterkey = "author__last_name"
            elif filterkey == "number":
                filterkey = "number_of_books_read"
            direction = request.GET.get("filterkey")
            direction = direction.split("_")[1]
            if direction == "desc":
                filterkey = f"-{filterkey}"
            myauthors = myauthors.order_by(filterkey)

        if "search" in request.GET:
            query = request.GET["search"]
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse("myauthors:myauthors"), pk=shelf_owner.pk)
            queries = Q(author__first_name__icontains=query) | Q(
                author__last_name__icontains=query
            )
            myauthors = myauthors.filter(queries)

    current_filterkey = f"{filter}_{direction}" if filter and direction else None
    paginator = Paginator(myauthors, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "shelf_owner": shelf_owner,
        "page_obj": page_obj,
        "myauthors_count": myauthors_count,
        "current_filterkey": current_filterkey,
    }
    return render(request, "myauthors/myauthor-list.html", context)


def myauthor_detail(request, pk):
    """
    View function for displaying a single author.
    """

    myauthor = MyAuthor.objects.get(pk=pk)
    mybooks = MyBook.objects.filter(user=pk, book__author=myauthor.author)
    context = {"myauthor": myauthor, "mybooks": mybooks}
    return render(request, "myauthors/myauthor.html", context)


def add_myauthor(request, author_id=None):
    """
    View function for adding an author to the user's shelf.
    """
    if request.method == "POST":
        form = MyAuthorForm(request.POST)
        if form.is_valid():
            myauthor = form.save(commit=False)
            myauthor.user = request.user
            myauthor.author.number_shelves += 1
            myauthor.save()
            messages.success(request, "Author added to your shelf")
            return redirect("myauthors:myauthor-detail", pk=myauthor.pk)
        else:
            messages.error(
                request, "There was an error adding the author to your shelf"
            )
    else:
        if author_id:
            author = Author.objects.get(pk=author_id)
            form = MyAuthorForm(initial={"author": author})
        else:
            form = MyAuthorForm()
    context = {
        "form": form,
        "object_name": "My Author",
    }
    return render(request, "generic-form.html", context)


def edit_myauthor(request, pk):
    """
    View function for editing an author on the user's shelf.
    """
    myauthor = MyAuthor.objects.get(pk=pk)
    if request.method == "POST":
        form = MyAuthorForm(request.POST, instance=myauthor)
        if form.is_valid():
            myauthor = form.save(commit=False)
            myauthor.user = request.user
            myauthor.save()
            messages.success(request, "Author updated successfully")
            return redirect("myauthors:myauthor-detail", pk=myauthor.pk)
        else:
            messages.error(request, "There was an error updating the author")
    else:
        form = MyAuthorForm(instance=myauthor)
    context = {
        "form": form,
        "object_name": myauthor.author.name,
        "edit": True,
    }
    return render(request, "generic-form.html", context)


def delete_myauthor(request, pk):
    """
    View function for deleting an author from the user's shelf.
    """
    myauthor = MyAuthor.objects.get(pk=pk)
    if request.method == "POST":
        myauthor.author.number_shelves -= 1
        myauthor.delete()
        messages.success(request, "The author has been deleted from your shelf")
        return redirect("myauthors:myauthors")
    return render(request, "delete-form.html", {"myauthor": myauthor})
