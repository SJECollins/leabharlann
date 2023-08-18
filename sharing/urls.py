from django.urls import path
from . import views


app_name = "sharing"
urlpatterns = [
    path("loaned-list/", views.loaned_list, name="loaned-list"),
    path("borrowed-list/", views.borrowed_list, name="borrowed-list"),
    path(
        "add-loaned/<int:pk>/",
        views.add_loaned,
        kwargs={"borrower_id": None},
        name="add-loaned",
    ),
    path("add-borrowed/<int:pk>/", views.add_borrowed, name="add-borrowed"),
    path("edit-loaned/<int:pk>/", views.edit_loaned, name="edit-loaned"),
    path("delete-loaned/<int:pk>/", views.delete_loaned, name="delete-loaned"),
    path("marked-returned/<int:pk>/", views.mark_returned, name="marked-returned"),
    path("request-list/", views.request_received_list, name="request-list"),
    path("request/<int:pk>/", views.request_received, name="request"),
    path(
        "request-accept/<int:pk>/", views.request_received_accept, name="request-accept"
    ),
    path(
        "request-reject/<int:pk>/", views.request_received_reject, name="request-reject"
    ),
    path("request-sent-list/", views.request_sent_list, name="request-sent-list"),
    path("request-sent/<int:pk>/", views.request_sent, name="request-sent"),
    path("request-send/<int:pk>/", views.request_send, name="request-send"),
]
