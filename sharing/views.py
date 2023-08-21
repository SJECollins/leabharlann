from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User

from mybooks.models import MyBook

from .models import ShareBook, ShareBookRequest
from .forms import (
    ShareBookLoanerForm,
    ShareBookBorrowerForm,
    ShareBookRequestAcceptForm,
    ShareBookRequestRejectForm,
    ShareBookReturnForm,
    ShareBookRequestForm,
)


def loaned_list(request):
    """
    View function for listing all loaned books on the user's shelf.
    """
    loaned = ShareBook.objects.filter(loaner=request.user).all()
    returned_count = loaned.filter(returned=True).count()
    shared_count = loaned.filter(returned=False).count()
    total_count = loaned.count()

    filter = None
    direction = None
    order_by = None

    if order_by is None and direction is None:
        loaned = loaned.order_by("-date_shared")

    if request.GET:
        order_by = request.GET.get("order_by")
        filter = order_by
        direction = request.GET.get("direction")
        if order_by == "title":
            order_by = "book__title"
        elif order_by == "borrow":
            order_by = "date_shared"
        elif order_by == "returned":
            order_by = "returned"
        elif order_by == "return-date":
            order_by = "date_returned"
        if direction == "desc":
            order_by = f"-{order_by}"
        loaned = loaned.order_by(order_by)

    current_sort = filter + "_" + direction if filter and direction else None
    print(current_sort)
    paginator = Paginator(loaned, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "share_list": "Loaned",
        "current_sort": current_sort,
        "shared_objects": page_obj,
        "total_count": total_count,
        "shared_count": shared_count,
        "returned_count": returned_count,
    }
    return render(request, "sharing/share-list.html", context)


def add_loaned(request, pk, borrower_id=None):
    """
    View function for adding a loaned book to the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        form = ShareBookLoanerForm(request.POST)
        if form.is_valid():
            loaned = form.save(commit=False)
            loaned.loaner = request.user
            loaned.save()
            messages.success(request, "Book added to your loaned list")
            return redirect("sharing:loaned-list", pk=mybook.pk)
        else:
            messages.error(
                request, "There was an error adding the book to your loaned list"
            )
    if borrower_id:
        borrower = User.objects.get(pk=borrower_id)
        form = ShareBookLoanerForm(initial={"borrower": borrower}, instance=mybook)
    else:
        form = ShareBookLoanerForm(instance=mybook)
    context = {
        "form": form,
        "object_name": mybook.book.title,
        "action_name": "Loan",
    }
    return render(request, "generic-form.html", context)


def edit_loaned(request, pk):
    """
    View function for editing a loaned book on the user's shelf.
    """
    loaned = ShareBook.objects.get(pk=pk)
    if request.method == "POST":
        form = ShareBookLoanerForm(request.POST, instance=loaned)
        if form.is_valid():
            loaned = form.save(commit=False)
            loaned.save()
            messages.success(request, "Book updated")
            return redirect("sharing:loaned-list", pk=loaned.pk)
        else:
            messages.error(request, "There was an error updating the book")
    else:
        form = ShareBookLoanerForm(instance=loaned)
    context = {
        "form": form,
        "object_name": loaned.book.title,
        "action_name": "Update loan of ",
    }
    return render(request, "generic-form.html", context)


def mark_returned(request, pk):
    """
    View function for toggling the returned status of a loaned book.
    """
    loaned = ShareBook.objects.get(pk=pk)
    if request.method == "POST":
        form = ShareBookReturnForm(request.POST, instance=loaned)
        if form.is_valid():
            loaned = form.save(commit=False)
            loaned.save()
            messages.success(request, "Book returned")
            return redirect("sharing:loaned-list", pk=loaned.pk)
        else:
            messages.error(request, "There was an error updating the book's status")
    form = ShareBookReturnForm(instance=loaned)
    context = {
        "form": form,
        "modal_title": f"Mark {loaned.book.title} as returned",
        "button_label": "Returned",
    }
    return render(request, "modal/modal-form.html", context)


def delete_loaned(request, pk):
    """
    View function for deleting a loaned book from the user's shelf.
    """
    loaned = ShareBook.objects.get(pk=pk)
    if request.method == "POST":
        loaned.delete()
        messages.success(request, "Book deleted from your loaned list")
        return redirect("sharing:loaned-list")
    context = {
        "object": loaned,
        "object_name": loaned.book.title,
    }
    return render(request, "delete-form.html", context)


def borrowed_list(request):
    """
    View function for listing all borrowed books on the user's shelf.
    """
    borrowed = ShareBook.objects.filter(borrower=request.user).order_by("-date_shared")
    returned_count = borrowed.filter(returned=True).count()
    borrowed_count = borrowed.filter(returned=False).count()
    total_count = borrowed.count()

    filter = None
    direction = None
    order_by = None

    if order_by is None and direction is None:
        borrowed = borrowed.order_by("-date_shared")

    if request.GET:
        order_by = request.GET.get("order_by")
        filter = order_by
        direction = request.GET.get("direction")
        if order_by == "title":
            order_by = "book__title"
        elif order_by == "borrow":
            order_by = "date_shared"
        elif order_by == "returned":
            order_by = "returned"
        elif order_by == "return-date":
            order_by = "date_returned"
        if direction == "desc":
            order_by = f"-{order_by}"
        borrowed = borrowed.order_by(order_by)

    current_sort = filter + "_" + direction if filter and direction else None
    print(current_sort)
    paginator = Paginator(borrowed, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "share_list": "Borrowed",
        "current_sort": current_sort,
        "shared_objects": page_obj,
        "total_count": total_count,
        "returned_count": returned_count,
        "shared_count": borrowed_count,
    }
    return render(request, "sharing/share-list.html", context)


def add_borrowed(request, pk):
    """
    View function for adding a borrowed book to the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        form = ShareBookBorrowerForm(request.POST)
        if form.is_valid():
            borrowed = form.save(commit=False)
            borrowed.borrower = request.user
            borrowed.save()
            messages.success(request, "Book added to your borrowed list")
            return redirect("sharing:borrowed-list", pk=mybook.pk)
        else:
            messages.error(
                request, "There was an error adding the book to your borrowed list"
            )
    form = ShareBookBorrowerForm(initial={"loaner": mybook.user}, instance=mybook)
    context = {
        "form": form,
        "object_name": mybook.book.title,
        "action_name": "Borrow",
    }
    return render(request, "generic-form.html", context)


def request_received_list(request):
    """
    View function for listing all requested books on the user's shelf.
    """
    requests = ShareBookRequest.objects.all().order_by("-date_requested")
    filter = None
    request_title = "All Requests"

    if filter is None:
        requests = requests.filter(loaner=request.user)
        requests_count = requests.count()
        request_title = "Requests Received"

    if request.GET:
        filterkey = request.GET.get("filterkey")
        if filterkey is None or filterkey == "default":
            requests = requests.filter(loaner=request.user)
        else:
            filter = filterkey
            if filterkey == "accepted":
                requests = requests.filter(accepted=True)
                request_title = "Requests Accepted"
            elif filterkey == "rejected":
                requests = requests.filter(rejected=True)
                request_title = "Requests Rejected"
            elif filterkey == "pending":
                requests = requests.filter(accepted=False, rejected=False)
                request_title = "Requests Pending"
            elif filterkey == "sent":
                requests = requests.filter(borrower=request.user)
                request_title = "Requests Sent"
            elif filterkey == "received":
                requests = requests.filter(loaner=request.user)
                request_title = "Requests Received"
        requests_count = requests.count()

    current_filterkey = filter if filter else None
    paginator = Paginator(requests, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "request_title": request_title,
        "request_url": "sharing:request-list",
        "current_filterkey": current_filterkey,
        "page_obj": page_obj,
        "requests_count": requests_count,
    }
    return render(request, "sharing/request-list.html", context)


def request_received(request, pk):
    """
    View function for displaying a single requested book on the user's shelf.
    """
    request_book = ShareBookRequest.objects.get(pk=pk)
    context = {"request_book": request_book}
    return render(request, "sharing/request.html", context)


def request_received_accept(request, pk):
    """
    View function for accepting a request for a book on the user's shelf.
    """
    request_book = ShareBookRequest.objects.get(pk=pk)
    if request.method == "POST":
        form = ShareBookRequestAcceptForm(request.POST, instance=request_book)
        if form.is_valid():
            request_book = form.save(commit=False)
            request_book.loaner = request.user
            request_book.save()
            messages.success(request, "Request accepted")
            return redirect("sharing:loaned", pk=request_book.pk)
        else:
            messages.error(request, "There was an error accepting the request")
    form = ShareBookRequestAcceptForm(instance=request_book)
    context = {
        "form": form,
        "modal_title": f"Accept request for {request_book.book.title}",
        "button_label": "Accept",
    }
    return render(request, "modal/modal-form.html", context)


def request_received_reject(request, pk):
    """
    View function for rejecting a request for a book on the user's shelf.
    """
    request_book = ShareBookRequest.objects.get(pk=pk)
    if request.method == "POST":
        form = ShareBookRequestRejectForm(request.POST, instance=request_book)
        if form.is_valid():
            request_book = form.save(commit=False)
            request_book.loaner = request.user
            request_book.save()
            messages.success(request, "Request rejected")
            return redirect("sharing:request-list")
        else:
            messages.error(request, "There was an error rejecting the request")
    form = ShareBookRequestRejectForm(instance=request_book)
    context = {
        "form": form,
        "modal_title": f"Reject request for {request_book.book.title}",
        "button_label": "Reject",
    }
    return render(request, "modal/modal-form.html", context)


def request_sent_list(request):
    """
    View function for listing all sent requests on the user's shelf.
    """
    requests = ShareBookRequest.objects.filter(borrower=request.user).order_by(
        "-date_requested"
    )
    requests_count = requests.count()
    context = {
        "requests": requests,
        "requests_count": requests_count,
    }
    return render(request, "sharing/request-list.html", context)


def request_sent(request, pk):
    """
    View function for displaying a single sent request on the user's shelf.
    """
    request_book = ShareBookRequest.objects.get(pk=pk)
    context = {"request_book": request_book}
    return render(request, "sharing/request.html", context)


def request_send(request, pk):
    """
    View function for sending a request for a book on the user's shelf.
    """
    mybook = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        form = ShareBookRequestForm(request.POST)
        if form.is_valid():
            request_book = form.save(commit=False)
            request_book.borrower = request.user
            request_book.save()
            messages.success(request, "Request sent")
            return redirect("sharing:request-sent", pk=request_book.pk)
        else:
            messages.error(request, "There was an error sending the request")
    form = ShareBookRequestForm(instance=mybook)
    context = {
        "form": form,
        "object_name": mybook.book.title,
        "action_name": "Request",
    }
    return render(request, "generic-form.html", context)
