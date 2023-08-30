from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form for adding and editing profiles.
    """

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "about_me", "profile_pic")


class InviteForm(forms.Form):
    """
    Form for inviting users to the site.
    """

    name = forms.CharField(help_text="Enter your friend's name")
    email = forms.EmailField(help_text="Enter your friend's email")
