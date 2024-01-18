from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from myauthors.models import MyAuthor

from mybooks.models import MyBook
from mygenres.models import MyGenre

from .models import Author, Book, Genre
from .forms import AuthorForm, BookForm, GenreForm


def author_list(request):
    """
    View function for listing all authors.
    Returns the authors ordered by name.
    """
    authors = Author.objects.all().order_by("name")
    author_count = authors.count()
    query = None
    filter = None
    direction = None

    if request.GET:
        filterkey = request.GET.get("filterkey")
        if filterkey is None or filterkey == "default":
            authors = authors.order_by("-created_on")
        else:
            filterkey = filterkey.split("_")[0]
            filter = filterkey
            if filterkey == "first":
                filterkey = "first_name"
            elif filterkey == "last":
                filterkey = "last_name"
            elif filterkey == "popularity":
                filterkey = "number_shelves"
            direction = request.GET.get("filterkey")
            direction = direction.split("_")[1]
            if direction == "desc":
                filterkey = f"-{filterkey}"
            authors = authors.order_by(filterkey)

        if "search" in request.GET:
            query = request.GET.get("search")
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse("books:author-list"))
            queries = (
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(name__icontains=query)
            )
            authors = authors.filter(queries)

    current_filterkey = filter + "_" + direction if filter and direction else None
    paginator = Paginator(authors, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        myauthors = MyAuthor.objects.filter(user=request.user)
        has_authors = [myauthor.author for myauthor in myauthors]

    context = {
        "page_obj": page_obj,
        "author_count": author_count,
        "current_filterkey": current_filterkey,
        "query_result": query if query else None,
        "has_authors": has_authors if request.user.is_authenticated else None,
    }
    return render(request, "books/author-list.html", context)


def author_detail(request, pk):
    """
    View function for displaying a single author.
    Returns the author object with the primary key (pk) equal to the pk argument.
    """
    author = Author.objects.get(pk=pk)
    books = Book.objects.filter(author=author)
    if request.user.is_authenticated:
        has_author = MyAuthor.objects.filter(user=request.user, author=author).first()

    context = {
        "author": author,
        "books": books,
        "has_author": has_author,
    }
    return render(request, "books/author.html", context)


def add_author(request):
    """
    View function for adding a new author.
    Passes the AuthorForm to the template.
    """
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.save()
            messages.success(request, "Author added successfully")
            return redirect("books:author-detail", pk=author.pk)
        else:
            messages.error(
                request, "There was a problem adding the author - please try again"
            )
    else:
        form = AuthorForm()
        context = {
            "form": form,
            "object_name": "An Author",
            "action_name": "Add",
        }
    return render(request, "generic-form.html", context)


def edit_author(request, pk):
    """
    View function for editing an author.
    Passes the instance argument to the AuthorForm.
    Returns the AuthorForm to the template.
    """
    author = Author.objects.get(pk=pk)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author = form.save(commit=False)
            author.save()
            messages.success(request, "Author edited successfully")
            return redirect("books:author-detail", pk=author.pk)
        else:
            messages.error(
                request, "There was a problem editing the author - please try again"
            )
    else:
        form = AuthorForm(instance=author)
        context = {
            "form": form,
            "object_name": author.name,
            "action_name": "Edit",
        }
    return render(request, "generic-form.html", context)


def book_list(request):
    """
    View function for listing all books.
    Returns the books ordered by title.
    """
    books = Book.objects.all().order_by("title")
    book_count = books.count()

    query = None
    filter = None
    direction = None

    if request.GET:
        filterkey = request.GET.get("filterkey")
        if filterkey is None or filterkey == "default":
            books = books.order_by("title")
        else:
            filterkey = filterkey.split("_")[0]
            filter = filterkey
            if filterkey == "author":
                filterkey = "author__name"
            elif filterkey == "genre":
                filterkey = "genre__name"
            elif filterkey == "title":
                filterkey = "title"
            elif filterkey == "popularity":
                filterkey = "number_shelves"
            direction = request.GET.get("filterkey")
            direction = direction.split("_")[1]
            if direction == "desc":
                filterkey = f"-{filterkey}"
            books = books.order_by(filterkey)

        if "search" in request.GET:
            query = request.GET.get("search")
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse("books:book-list"))
            queries = (
                Q(title__icontains=query)
                | Q(author__name__icontains=query)
                | Q(genre__name__icontains=query)
            )
            books = books.filter(queries)

    current_filterkey = filter + "_" + direction if filter and direction else None
    paginator = Paginator(books, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        mybooks = MyBook.objects.filter(user=request.user)
        has_books = [mybook.book for mybook in mybooks]

    context = {
        "page_obj": page_obj,
        "book_count": book_count,
        "current_filterkey": current_filterkey,
        "query_result": query if query else None,
        "has_books": has_books if request.user.is_authenticated else None,
    }
    return render(request, "books/book-list.html", context)


def book_detail(request, pk):
    """
    View function for displaying a single book.
    Returns the book object with the primary key (pk) equal to the pk argument.
    """
    book = Book.objects.get(pk=pk)
    has_book = None
    if request.user.is_authenticated:
        has_book = MyBook.objects.filter(user=request.user, book=book).first()

    context = {
        "book": book,
        "has_book": has_book,
    }
    return render(request, "books/book.html", context)


def add_book(request):
    """
    View function for adding a new book.
    Sends the BookForm to the template.
    Passes the request.POST and request.FILES arguments to the BookForm.
    """
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            messages.success(request, "Book added successfully")
            return redirect("books:book-detail", pk=book.pk)
        else:
            messages.error(
                request, "There was a problem adding the book - please try again"
            )
    else:
        form = BookForm()
    return render(request, "books/book-form.html", {"form": form})


def edit_book(request, pk):
    """
    View function for editing a book.
    Returns the BookForm to the template.
    Returns the book object with the primary key (pk) equal to the pk argument.
    """
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            if Book.objects.filter(title=book.title, author=book.author).exists():
                messages.error(
                    request,
                    "This book already exists - please check the list of books or try again with a different title or author",
                )
                return redirect("book-list")
            else:
                book.save()
                messages.success(request, "Book edited successfully")
                return redirect("books:book-detail", pk=book.pk)
        else:
            messages.error(
                request, "There was a problem editing the book - please try again"
            )
    else:
        form = BookForm(instance=book)
        context = {
            "form": form,
            "object_name": book.title,
            "action_name": "Edit",
        }
    return render(request, "generic-form.html", context)


def genre_list(request):
    """
    View function for listing all genres.
    Returns the genres ordered by name and the number of genres.
    """
    genres = Genre.objects.all().order_by("name")
    genre_count = genres.count()

    query = None
    filter = None
    direction = None

    if request.GET:
        filterkey = request.GET.get("filterkey")
        if filterkey is None or filterkey == "default":
            genres = genres.order_by("name")
        else:
            filterkey = filterkey.split("_")[0]
            filter = filterkey
            if filterkey == "popularity":
                filterkey = "number_shelves"
            elif filterkey == "name":
                filterkey = "name"
            direction = request.GET.get("filterkey")
            direction = direction.split("_")[1]
            if direction == "desc":
                filterkey = f"-{filterkey}"
            genres = genres.order_by(filterkey)

        if "search" in request.GET:
            query = request.GET.get("search")
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse("books:genre-list"))
            queries = Q(name__icontains=query)
            genres = genres.filter(queries)

    current_filterkey = filter + "_" + direction if filter and direction else None
    paginator = Paginator(genres, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        mygenres = MyGenre.objects.filter(user=request.user)
        has_genres = [mygenre.genre for mygenre in mygenres]

    context = {
        "page_obj": page_obj,
        "genre_count": genre_count,
        "current_filterkey": current_filterkey,
        "query_result": query if query else None,
        "has_genres": has_genres if request.user.is_authenticated else None,
    }
    return render(request, "books/genre-list.html", context)


def genre_detail(request, pk):
    """
    View function for displaying a single genre.
    Returns the genre object with the primary key (pk) equal to the pk argument.
    """
    genre = Genre.objects.get(pk=pk)
    if request.user.is_authenticated:
        has_genre = MyGenre.objects.filter(user=request.user, genre=genre).first()
    books = Book.objects.filter(genre=genre)
    context = {
        "genre": genre,
        "books": books,
        "has_genre": has_genre,
    }
    return render(request, "books/genre.html", context)


def add_genre(request):
    """
    View function for adding a new genre.
    Passes the GenreForm to the template.
    """
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save(commit=False)
            if Genre.objects.filter(name=genre.name).exists():
                messages.error(
                    request,
                    "This genre already exists - please check the list of genres or try again with a different name",
                )
                return redirect("genre-list")
            else:
                genre.save()
                messages.success(request, "Genre added successfully")
                return redirect("books:genre-detail", pk=genre.pk)
        else:
            messages.error(
                request, "There was a problem adding the genre - please try again"
            )
    else:
        form = GenreForm()
        context = {
            "form": form,
            "object_name": "A Genre",
            "action_name": "Add",
        }
    return render(request, "generic-form.html", context)


def edit_genre(request, pk):
    """
    View function for editing a genre.
    Passes the instance argument to the GenreForm.
    Returns the GenreForm to the template.
    """
    genre = Genre.objects.get(pk=pk)
    if request.method == "POST":
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            genre = form.save(commit=False)
            genre.save()
            messages.success(request, "Genre edited successfully")
            return redirect("books:genre-detail", pk=genre.pk)
        else:
            messages.error(
                request, "There was a problem editing the genre - please try again"
            )
    else:
        form = GenreForm(instance=genre)
        context = {
            "form": form,
            "object_name": genre.name,
            "action_name": "Edit",
        }
    return render(request, "generic-form.html", context)
