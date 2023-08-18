from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from leabharlann.utils import edit_image


class Profile(models.Model):
    """
    Model representing a user profile.
    Fields to be displayed are user, first_name, last_name, about_me, profile_pic.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=50, blank=True, help_text="Optional. Enter your first name"
    )
    last_name = models.CharField(
        max_length=50, blank=True, help_text="Optional. Enter your last name"
    )
    about_me = models.TextField(
        max_length=500, blank=True, help_text="Optional. Tell us about yourself"
    )
    profile_pic = models.ImageField(
        upload_to="profile_pics",
        blank=True,
        help_text="Optional. Upload a profile picture",
    )
    joined_on = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(
        default=False,
        help_text="If checked, your profile will not be visible to other users",
    )
    friends = models.ManyToManyField(
        User,
        blank=True,
        related_name="friends",
        help_text="Select the users you want to be friends with",
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        """
        Override the save method of the Profile model to resize the profile pic.
        """
        if self.profile_pic:
            self.profile_pic = edit_image(self.profile_pic, 100, 100)
        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile.
    """
    if created:
        Profile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.profile.save()


class FriendRequest(models.Model):
    """
    Model representing a friend request.
    Fields to be displayed are from_user, to_user, accepted.
    """

    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="from_user"
    )
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    sent = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} to {self.to_user}"

    def save(self, *args, **kwargs):
        """
        Override the save method of the FriendRequest model to prevent duplicate requests.
        """
        if FriendRequest.objects.filter(
            from_user=self.from_user, to_user=self.to_user
        ).exists():
            raise ValueError("You have already sent a friend request to this user")
        if self.accepted:
            self.from_user.profile.friends.add(self.to_user)
            self.to_user.profile.friends.add(self.from_user)
        super(FriendRequest, self).save(*args, **kwargs)
