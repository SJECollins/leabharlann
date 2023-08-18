from django import forms
from books.models import Author
from .models import MyAuthor


class MyAuthorForm(forms.ModelForm):
    """
    ModelForm for the MyAuthor model.
    Allows the user to add an author to their shelf.
    Extra fields are honorific, first_name, middle_name, last_name to create a new author.
    """

    honorific = forms.CharField(max_length=10, required=False)
    first_name = forms.CharField(max_length=100, required=False)
    middle_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = MyAuthor
        fields = ["author", "notes", "favourite"]

    def __init__(self, *args, **kwargs):
        super(MyAuthorForm, self).__init__(*args, **kwargs)
        self.fields["author"].required = False
        self.fields["honorific"].label = "Honorific"
        self.fields["first_name"].label = "First name"
        self.fields["middle_name"].label = "Middle name"
        self.fields["last_name"].label = "Last name"

    def clean(self):
        cleaned_data = super(MyAuthorForm, self).clean()
        existing_author = cleaned_data.get("author")
        honorific = cleaned_data.get("honorific")
        first_name = cleaned_data.get("first_name")
        middle_name = cleaned_data.get("middle_name")
        last_name = cleaned_data.get("last_name")
        if existing_author:
            cleaned_data["author"] = existing_author
            return cleaned_data
        elif not existing_author:
            if not first_name:
                raise forms.ValidationError("You must enter a first name")
            if not last_name:
                raise forms.ValidationError("You must enter a last name")
            author, created = Author.objects.get_or_create(
                honorific=honorific,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
            )
            cleaned_data["author"] = author
            return cleaned_data
