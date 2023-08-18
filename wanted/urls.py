from django.urls import path
from . import views


app_name = "wanted"
urlpatterns = [
    path("wanted/<int:pk>/", views.wanted, name="wanted"),
    path("add-wanted/", views.add_wanted, kwargs={"book_id": None}, name="add-wanted"),
    path("edit-wanted/<int:pk>/", views.edit_wanted, name="edit-wanted"),
    path("delete-wanted/<int:pk>/", views.delete_wanted, name="delete-wanted"),
]
