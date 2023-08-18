from django.shortcuts import redirect, render
from django.contrib import messages

from books.models import Book
from .models import MyBookReview
from .forms import MyBookReviewForm


def review_list(request):
    """
    View function for listing all public reviews.
    Returns the reviews ordered by date added and the review count.
    Filter the reviews to only show public reviews.
    """
    reviews = MyBookReview.objects.filter(private=False).order_by("-date_added")[:10]
    review_count = reviews.count()
    context = {"reviews": reviews, "review_count": review_count}
    return render(request, "review/review-list.html", context)


def book_review_list(request, pk):
    """
    View function for listing all reviews for a specific book.
    Returns the reviews for the book ordered by date added and the review count.
    """
    reviews = MyBookReview.objects.filter(book=pk).order_by("-date_added")
    review_count = reviews.count()
    context = {"reviews": reviews, "review_count": review_count}
    return render(request, "review/review-list.html", context)


def review_detail(request, pk):
    """
    View function for displaying a single review.
    Returns the review object with the primary key (pk) equal to the pk argument.
    """
    review = MyBookReview.objects.get(pk=pk)
    return render(request, "review/review.html", {"review": review})


def add_review(request, pk):
    """
    View function for adding a new review.
    Returns the ReviewForm to the template.
    Passes the book object to the template.
    """
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        form = MyBookReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Review added successfully")
            return redirect("review:review-detail", pk=review.pk)
        else:
            messages.error(request, "Error adding review")
    else:
        form = MyBookReviewForm(initial={"book": book})
        context = {
            "form": form,
            "modal_title": f"Add Review For {book.title}",
            "button_label": "Add Review",
        }
    return render(request, "modal/modal-form.html", context)


def edit_review(request, pk):
    """
    View function for editing a review.
    Passes the instance argument to the ReviewForm.
    Returns the ReviewForm to the template.
    """
    review = MyBookReview.objects.get(pk=pk)
    if request.user != review.user:
        return render(request, "review/review-list.html")
    else:
        if request.method == "POST":
            form = MyBookReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.save()
                messages.success(request, "Review edited successfully")
                return redirect("review:review-detail", pk=review.pk)
            else:
                messages.error(request, "Error editing review")
        else:
            form = MyBookReviewForm(instance=review)
            context = {"form": form, "review": review}
        return render(request, "modal/modal-form.html", context)


def delete_review(request, pk):
    """
    View function for deleting a review.
    Returns the ReviewForm to the template.
    User is asked to confirm they want to delete the review.
    User must be the author of the review to delete it.
    """
    review = MyBookReview.objects.get(pk=pk)
    if request.user != review.user:
        return render(request, "review/review-list.html")
    else:
        if request.method == "POST":
            review.delete()
            messages.success(request, "Review deleted successfully")
            return redirect("shelf:myshelf", pk=request.user.pk)
        else:
            context = {"object": review, "object_name": review.book.title}
        return render(request, "delete-form.html", context)
