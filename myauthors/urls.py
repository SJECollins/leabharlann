from django.urls import path

from . import views

app_name = "myauthors"
urlpatterns = [
    path("myauthors/<int:pk>/", views.my_authors, name="myauthors"),
    path("myauthor-detail/<int:pk>/", views.myauthor_detail, name="myauthor-detail"),
    path(
        "add-myauthor/",
        views.add_myauthor,
        kwargs={"author_id": None},
        name="add-myauthor",
    ),
    path("add-myauthor/<int:author_id>/", views.add_myauthor, name="add-myauthor"),
    path("edit-myauthor/<int:pk>/", views.edit_myauthor, name="edit-myauthor"),
    path("delete-myauthor/<int:pk>/", views.delete_myauthor, name="delete-myauthor"),
]
