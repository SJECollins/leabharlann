from django.shortcuts import render
from django.contrib.auth.models import User

from mybooks.models import MyBook
from wanted.models import Wanted


def my_shelf(request, pk):
    """
    View function for listing all books on the user's shelf.
    Returns the books the user is currently reading, books the user has finished reading,
    their wanted books, the book count, the number of books finished, and the number of wanted books.
    """
    shelf_owner = User.objects.get(pk=pk)
    mybooks = MyBook.objects.filter(user=pk).order_by("-added_on")
    currently_reading = mybooks.filter(currently_reading=True)
    recently_finished = mybooks.filter(finished=True).order_by("-finished_reading_on")[
        :5
    ]
    wanted = Wanted.objects.filter(user=pk).order_by("-added_on")[:5]
    context = {
        "shelf_owner": shelf_owner,
        "mybooks_count": mybooks.count(),
        "finished_count": mybooks.filter(finished=True).count(),
        "currently_reading": currently_reading,
        "recently_finished": recently_finished,
        "wanted": wanted,
        "wanted_count": wanted.count(),
    }
    return render(request, "shelf/myshelf.html", context)
