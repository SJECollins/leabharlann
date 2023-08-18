from django.urls import path
from . import views


app_name = "review"
urlpatterns = [
    path("review-list/", views.review_list, name="review-list"),
    path("book-review-list/<int:pk>/", views.book_review_list, name="book-review-list"),
    path("review/<int:pk>/", views.review_detail, name="review-detail"),
    path("add-review/<int:pk>/", views.add_review, name="add-review"),
    path("edit-review/<int:pk>/", views.edit_review, name="edit-review"),
    path("delete-review/<int:pk>/", views.delete_review, name="delete-review"),
]
