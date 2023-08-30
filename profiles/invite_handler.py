from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Profile


def handle_invite(request, pk, name, email):
    profile = Profile.objects.get(pk=pk)

    if profile.first_name is None:
        user = profile.user.username
    else:
        user = profile.first_name + " " + profile.last_name

    subject = render_to_string(
        "profiles/invite-email/invite-subject.txt", {"user": user}
    )
    body = render_to_string(
        "profiles/invite-email/invite-body.txt", {"user": user, "name": name}
    )
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
