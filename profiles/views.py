from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile, FriendRequest
from .forms import ProfileForm, InviteForm

from .invite_handler import handle_invite


def profile_list(request):
    """
    View function for listing all profiles.
    Returns the profiles ordered by name and the profile count.
    """
    profiles = Profile.objects.all().order_by("name")
    profile_count = profiles.count()
    context = {"profiles": profiles, "profile_count": profile_count}
    return render(request, "profiles/profile-list.html", context)


def profile_detail(request, pk):
    """
    View function for displaying a single profile.
    Returns the profile object with the primary key (pk) equal to the pk argument.
    """
    profile = Profile.objects.get(pk=pk)
    friends = profile.friends.all()[:5]
    friend_request = FriendRequest.objects.filter(
        to_user=pk, from_user=request.user
    ).first()
    context = {"profile": profile, "friends": friends, "friend_request": friend_request}
    return render(request, "profiles/profile.html", context)


def edit_profile(request):
    """
    View function for editing a profile.
    Passes the instance argument to the ProfileForm.
    Returns the ProfileForm to the template.
    """
    profile = Profile.objects.get(user=request.user)
    if request.user != profile.user:
        return render(request, "profiles/profile-list.html")
    else:
        if request.method == "POST":
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.save()
                messages.success(request, "Profile updated successfully")
                return redirect("profiles:profile-detail", pk=profile.pk)
            else:
                messages.error(request, "Error updating profile")
        else:
            form = ProfileForm(instance=profile)
        context = {
            "form": form,
            "object_name": "My Profile",
            "action_name": "Edit",
        }
        return render(request, "generic-form.html", context)


def toggle_private(request, pk):
    """
    View function for toggling the private status of a profile.
    Returns the profile object with the primary key (pk) equal to the pk argument.
    """
    profile = Profile.objects.get(pk=pk)
    profile.private = not profile.private
    profile.save()
    return redirect("profiles:profile-detail", pk=profile.pk)


def friend_list(request, pk):
    """
    View function for listing all friends.
    Returns the friends of the current user.
    """
    if request.GET:
        query = request.GET.get("search")
        if query:
            results = User.objects.filter(username__icontains=query, private=False)
            context = {
                "results": results,
                "query": query,
            }
            return render(request, "profiles/friend-list.html", context)

    profile = Profile.objects.get(user=pk)
    friends = profile.friends.all()
    context = {"friends": friends}
    return render(request, "profiles/friend-list.html", context)


def invite_friend(request, pk):
    """
    View function for sending an email to invite a friend outside the site.
    """

    if request.method == "POST":
        handle_invite(request, pk, request.POST.get("name"), request.POST.get("email"))
        messages.success(request, "Invitation sent")
        return HttpResponse(status=204)

    form = InviteForm()
    context = {
        "form": form,
        "modal_title": "Invite a friend",
        "button_label": "Send invitation",
    }
    return render(request, "modal/modal-form.html", context)


def send_friend_request(request, pk):
    """
    View function for sending a friend request.
    Returns the profile object with the primary key (pk) equal to the pk argument.
    """
    to_user = User.objects.get(pk=pk)
    friend_request, created = FriendRequest.objects.get_or_create(
        from_user=request.user, to_user=to_user
    )
    if created:
        messages.success(request, "Friend request sent")
    else:
        messages.error(request, "You have already sent a friend request to this user")
    return redirect("profiles:profile-detail", pk=pk)


def friend_requests(request):
    """
    View function for listing all friend requests.
    Returns the friend requests of the current user.
    """
    friend_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    context = {"friend_requests": friend_requests}
    return render(request, "profiles/friend-request-list.html", context)


def friend_request_detail(request, pk):
    """
    View function for displaying a single friend request.
    Returns the friend request object with the primary key (pk) equal to the pk argument.
    """
    friend_request = FriendRequest.objects.get(pk=pk)
    context = {"friend_request": friend_request}
    return render(request, "modal/friend-request.html", context)


def accept_friend_request(request, pk):
    """
    View function for accepting a friend request.
    Returns the profile object with the primary key (pk) equal to the pk argument.
    """
    if request.method == "POST":
        friend_request = FriendRequest.objects.get(pk=pk)
        friend_request.accepted = True
        friend_request.save()
        messages.success(request, "Friend request accepted")
        return HttpResponse(status=204)
    else:
        messages.error(request, "Error accepting friend request")


def reject_friend_request(request, pk):
    """
    View function for rejecting a friend request.
    Returns the profile object with the primary key (pk) equal to the pk argument.
    """
    if request.method == "POST":
        friend_request = FriendRequest.objects.get(pk=pk)
        friend_request.delete()
        messages.success(request, "Friend request rejected")
        return HttpResponse(status=204)
    else:
        messages.error(request, "Error rejecting friend request")


def unfriend(request, pk):
    """
    View function for removing a friend.
    Returns the profile object with the primary key (pk) equal to the pk argument.
    """
    profile = Profile.objects.get(pk=pk)
    profile.friends.remove(request.user)
    request.user.profile.friends.remove(profile.user)
    messages.success(request, "Friend removed")
    return redirect("profiles:profile-detail", pk=pk)
