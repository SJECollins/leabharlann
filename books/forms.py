from django import forms

from .models import Author, Book, Genre


class AuthorForm(forms.ModelForm):
    """
    Form for adding and editing authors.
    """

    class Meta:
        model = Author
        fields = ["honorific", "first_name", "middle_name", "last_name"]


class BookForm(forms.ModelForm):
    """
    Form for adding and editing books.
    """

    author_first = forms.CharField(max_length=100, required=False)
    author_last = forms.CharField(max_length=100, required=False)
    new_genre = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Book
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields["author"].required = False
        self.fields["author_first"].label = "New author first name"
        self.fields["author_last"].label = "New author last name"
        self.fields["new_genre"].label = "New genre"

    def clean(self):
        cleaned_data = super(BookForm, self).clean()
        existing_author = cleaned_data.get("author")
        new_author_first = cleaned_data.get("author_first")
        new_author_last = cleaned_data.get("author_last")
        new_author = None
        if existing_author and new_author_first and new_author_last:
            raise forms.ValidationError(
                "You can't select an existing author and enter a new author"
            )
        if not existing_author and not new_author_first and not new_author_last:
            raise forms.ValidationError(
                "You must select an existing author or enter a new author"
            )
        if new_author_first and new_author_last:
            new_author = Author.objects.filter(
                first_name=new_author_first, last_name=new_author_last
            ).first()
            if new_author:
                raise forms.ValidationError("Author already exists")
            else:
                new_author = Author.objects.create(
                    first_name=new_author_first, last_name=new_author_last
                )
        if existing_author:
            cleaned_data["author"] = existing_author
            return cleaned_data
        elif new_author:
            cleaned_data["author"] = new_author
            return cleaned_data
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
            genre = Genre.objects.filter(name=new_genre).first()
            if genre:
                raise forms.ValidationError("Genre already exists")
            else:
                create_genre = Genre.objects.create(name=new_genre)
                cleaned_data["genre"] = create_genre
                return cleaned_data


class GenreForm(forms.ModelForm):
    """
    Form for adding and editing genres.
    """

    class Meta:
        model = Genre
        fields = ("name",)
