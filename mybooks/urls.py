from django.urls import path
from . import views


app_name = "mybooks"
urlpatterns = [
    path("mybooks/<int:pk>", views.my_books, name="mybooks"),
    path("mybook-detail/<int:pk>/", views.mybook_detail, name="mybook-detail"),
    path("add-mybook/", views.add_mybook, kwargs={"book_id": None}, name="add-mybook"),
    path("add-mybook/<int:book_id>/", views.add_mybook, name="add-mybook"),
    path("edit-mybook/<int:pk>/", views.edit_mybook, name="edit-mybook"),
    path("start-reading/<int:pk>/", views.start_reading, name="start"),
    path("update-progress/<int:pk>/", views.update_progress, name="update-progress"),
    path("update-notes/<int:pk>/", views.update_notes, name="update-notes"),
    path("update-summary/<int:pk>/", views.update_summary, name="update-summary"),
    path("mark-finished/<int:pk>/", views.mark_finished, name="finish"),
    path("mark-abandoned/<int:pk>/", views.mark_abandoned, name="abandon"),
    path("toggle-favourite/<int:pk>/", views.toggle_favourite, name="favourite"),
    path("toggle-private/<int:pk>/", views.toggle_private, name="private"),
    path("delete-book/<int:pk>/", views.delete_mybook, name="delete-book"),
]
