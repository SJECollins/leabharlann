from django.urls import path
from . import views


app_name = "books"
urlpatterns = [
    path("author-list/", views.author_list, name="author-list"),
    path("author/<int:pk>/", views.author_detail, name="author-detail"),
    path("add-author/", views.add_author, name="add-author"),
    path("edit-author/<int:pk>/", views.edit_author, name="edit-author"),
    path("book-list/", views.book_list, name="book-list"),
    path("book/<int:pk>/", views.book_detail, name="book-detail"),
    path("add-book/", views.add_book, name="add-book"),
    path("edit-book/<int:pk>/", views.edit_book, name="edit-book"),
    path("genre-list/", views.genre_list, name="genre-list"),
    path("genre/<int:pk>/", views.genre_detail, name="genre-detail"),
    path("add-genre/", views.add_genre, name="add-genre"),
    path("edit-genre/<int:pk>/", views.edit_genre, name="edit-genre"),
]
