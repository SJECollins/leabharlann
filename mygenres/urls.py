from django.urls import path
from . import views

app_name = "mygenres"
urlpatterns = [
    path("mygenres/<int:pk>/", views.my_genres, name="mygenres"),
    path("mygenre-detail/<int:pk>/", views.mygenre_detail, name="mygenre-detail"),
    path(
        "add-mygenre/", views.add_mygenre, kwargs={"genre_id": None}, name="add-mygenre"
    ),
    path("add-mygenre/<int:genre_id>/", views.add_mygenre, name="add-mygenre"),
    path("edit-mygenre/<int:pk>/", views.edit_mygenre, name="edit-mygenre"),
    path("delete-mygenre/<int:pk>/", views.delete_mygenre, name="delete-mygenre"),
]
