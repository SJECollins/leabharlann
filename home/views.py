from django.shortcuts import render
from books.models import Book, Author, Genre
from mybooks.models import MyBook
from .models import ContactMessage


def index(request):
    """
    A view to return the index page
    """
    if request.user.is_authenticated:
        current_book = (
            MyBook.objects.filter(user=request.user, currently_reading=True)
            .order_by("started_reading_on")
            .first()
        )
        popular_books = Book.objects.all().order_by("-number_reads")[:5]
        popular_authors = Author.objects.all().order_by("-number_reads")[:5]
        popular_genres = Genre.objects.all().order_by("-number_reads")[:5]
        context = {
            "current_book": current_book,
            "popular_books": popular_books,
            "popular_authors": popular_authors,
            "popular_genres": popular_genres,
        }
        return render(request, "home/index.html", context)
    return render(request, "home/index.html")


def about(request):
    """
    A view to return the about page
    """
    return render(request, "home/about.html")


def contact(request):
    """
    A view to return the contact page
    """
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name, email=email, subject=subject, message=message
        )
        return render(request, "home/contact.html", {"success": True})

    return render(request, "home/contact.html")


def faqs(request):
    """
    A view to return the faqs page
    """
    return render(request, "home/faqs.html")
