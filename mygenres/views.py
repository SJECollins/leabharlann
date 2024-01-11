from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from books.models import Genre


from mybooks.models import MyBook
from .models import MyGenre
from .forms import MyGenreForm


def my_genres(request, pk=None):
    """
    View function for listing all genres on the user's shelf.
    """
    shelf_owner = User.objects.get(pk=pk)
    mygenres = MyGenre.objects.filter(user=shelf_owner).order_by("genre__name")
    mygenres_count = mygenres.count()

    query = None
    filter = None
    direction = None

    if request.GET:
        filterkey = request.GET.get("filterkey")
        if filterkey is None or filterkey == "default":
            mygenres = mygenres.order_by("genre__name")
        else:
            filterkey = filterkey.split("_")[0]
            filter = filterkey
            if filterkey == "name":
                filterkey = "genre__name"
            elif filterkey == "number":
                filterkey = "number_of_books_read"
            direction = request.GET.get("filterkey")
            direction = direction.split("_")[1]
            if direction == "desc":
                filterkey = f"-{filterkey}"
            mygenres = mygenres.order_by(filterkey)

        if "search" in request.GET:
            query = request.GET["search"]
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse("mygenres:mygenres"))
            queries = Q(genre__name__icontains=query)
            mygenres = mygenres.filter(queries)

    current_filterkey = f"{filter}_{direction}" if filter and direction else None
    paginator = Paginator(mygenres, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "shelf_owner": shelf_owner,
        "page_obj": page_obj,
        "mygenres_count": mygenres_count,
        "current_filterkey": current_filterkey,
    }
    return render(request, "mygenres/mygenre-list.html", context)


def mygenre_detail(request, pk, user_id=None):
    """
    View function for displaying a single genre.
    """
    mygenre = MyGenre.objects.get(pk=pk)
    mybooks = MyBook.objects.filter(user=user_id, book__genre=mygenre.genre.id)
    context = {"mygenre": mygenre, "mybooks": mybooks}
    return render(request, "mygenres/mygenre.html", context)


def add_mygenre(request, genre_id=None):
    """
    View function for adding a genre to the user's shelf.
    """
    if request.method == "POST":
        form = MyGenreForm(request.POST)
        if form.is_valid():
            mygenre = form.save(commit=False)
            mygenre.user = request.user
            mygenre.genre.number_shelves += 1
            mygenre.save()
            messages.success(request, "Genre added to your shelf")
            return redirect("mygenres:mygenre-detail", pk=mygenre.pk)
        else:
            messages.error(request, "There was an error adding the genre to your shelf")
    else:
        if genre_id:
            genre = Genre.objects.get(pk=genre_id)
            form = MyGenreForm(initial={"genre": genre})
        else:
            form = MyGenreForm()
    context = {
        "form": form,
        "object_name": "My Genre",
    }
    return render(request, "generic-form.html", context)


def edit_mygenre(request, pk):
    """
    View function for editing a genre on the user's shelf.
    """
    mygenre = MyGenre.objects.get(pk=pk)
    if request.method == "POST":
        form = MyGenreForm(request.POST, instance=mygenre)
        if form.is_valid():
            mygenre = form.save(commit=False)
            mygenre.user = request.user
            mygenre.save()
            messages.success(request, "Genre updated successfully")
            return redirect("mygenres:mygenre-detail", pk=mygenre.pk)
        else:
            messages.error(request, "There was an error updating the genre")
    else:
        form = MyGenreForm(instance=mygenre)
    context = {
        "form": form,
        "object_name": mygenre.genre.name,
        "edit": True,
    }
    return render(request, "generic-form.html", context)


def delete_mygenre(request, pk):
    """
    View function for deleting a genre from the user's shelf.
    """
    mygenre = MyGenre.objects.get(pk=pk)
    if request.method == "POST":
        mygenre.genre.number_shelves -= 1
        mygenre.delete()
        messages.success(request, "The genre has been deleted from your shelf")
        return redirect("mygenres:mygenres")
    return render(request, "delete-form.html", {"mygenre": mygenre})
