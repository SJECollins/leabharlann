from django.urls import path
from . import views


app_name = "shelf"
urlpatterns = [
    path("my-shelf/<int:pk>", views.my_shelf, name="myshelf"),
]
