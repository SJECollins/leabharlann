from django.urls import path
from . import views


app_name = "profiles"
urlpatterns = [
    path("profile-list/", views.profile_list, name="profile-list"),
    path("profile/<int:pk>/", views.profile_detail, name="profile-detail"),
    path("edit-profile/", views.edit_profile, name="edit-profile"),
    path(
        "toggle-profile-private/<int:pk>/",
        views.toggle_private,
        name="toggle-profile-private",
    ),
    path("friend-list/<int:pk>/", views.friend_list, name="friend-list"),
    path(
        "friend-request-detail/<int:pk>/",
        views.friend_request_detail,
        name="friend-request-detail",
    ),
    path(
        "send-friend-request/<int:pk>/",
        views.send_friend_request,
        name="send-friend-request",
    ),
    path("friend-request-list/", views.friend_requests, name="friend-request-list"),
    path(
        "accept-friend-request/<int:pk>/",
        views.accept_friend_request,
        name="accept-friend-request",
    ),
    path(
        "reject-friend-request/<int:pk>/",
        views.reject_friend_request,
        name="reject-friend-request",
    ),
    path("unfriend/<int:pk>/", views.unfriend, name="unfriend"),
]
