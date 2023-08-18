from django import forms

from books.models import Genre
from .models import MyGenre


class MyGenreForm(forms.ModelForm):
    """
    ModelForm to edit the MyGenre model.
    Extra field to add a new genre.
    """

    new_genre = forms.CharField(
        max_length=100, required=False, help_text="Can't find your genre? Add it here"
    )

    class Meta:
        model = MyGenre
        fields = ["genre", "notes", "favourite"]

    def __init__(self, *args, **kwargs):
        super(MyGenreForm, self).__init__(*args, **kwargs)
        self.fields["genre"].required = False
        self.fields["new_genre"].label = "New genre"

    def clean(self):
        cleaned_data = super(MyGenreForm, self).clean()
        existing_genre = cleaned_data.get("genre")
        new_genre = cleaned_data.get("new_genre")
        if existing_genre and new_genre:
            raise forms.ValidationError(
                "You can't select an existing genre and enter a new genre"
            )
        if not existing_genre and not new_genre:
            raise forms.ValidationError(
                "You must select an existing genre or enter a new genre"
            )
        if existing_genre:
            cleaned_data["genre"] = existing_genre
            return cleaned_data
        elif new_genre:
            genre, created = Genre.objects.get_or_create(name=new_genre)
            cleaned_data["genre"] = genre
            return cleaned_data
