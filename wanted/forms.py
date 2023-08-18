from django import forms

from books.models import Author, Book, Genre
from .models import Wanted


class WantedForm(forms.ModelForm):
    """
    ModelForm to create a Wanted model.
    Extra fields are added to allow the user to enter a new book.
    """

    new_book = forms.CharField(max_length=140, required=False)
    author_first = forms.CharField(max_length=100, required=False)
    author_last = forms.CharField(max_length=100, required=False)
    genre = forms.CharField(max_length=100, required=False)
    book_cover = forms.ImageField(required=False)

    class Meta:
        model = Wanted
        fields = ["book", "notes", "private"]

    def __init__(self, *args, **kwargs):
        super(WantedForm, self).__init__(*args, **kwargs)
        self.fields["book"].required = False
        self.fields["new_book"].label = "Book title"
        self.fields["author_first"].label = "Author first name"
        self.fields["author_last"].label = "Author last name"
        self.fields["genre"].label = "Genre"
        self.fields["book_cover"].label = "Book cover"

    def clean(self):
        cleaned_data = super(WantedForm, self).clean()
        print(cleaned_data)
        existing_book = cleaned_data.get("book")
        new_book = cleaned_data.get("new_book")
        print(new_book)
        if existing_book and new_book:
            raise forms.ValidationError(
                "You can't select an existing book and enter a new book"
            )
        if not existing_book and not new_book:
            raise forms.ValidationError(
                "You must select an existing book or enter a new book"
            )
        if existing_book:
            cleaned_data["book"] = existing_book
            return cleaned_data
        elif new_book:
            book = Book.objects.filter(title=new_book).first()
            if book:
                raise forms.ValidationError("Book already exists")
            else:
                if not cleaned_data.get("author_first"):
                    raise forms.ValidationError("You must enter an author first name")
                if not cleaned_data.get("author_last"):
                    raise forms.ValidationError("You must enter an author last name")
                if not cleaned_data.get("genre"):
                    raise forms.ValidationError("You must enter a genre")
                author, created = Author.objects.get_or_create(
                    first_name=cleaned_data.get("author_first"),
                    last_name=cleaned_data.get("author_last"),
                )
                print(author)
                genre, created = Genre.objects.get_or_create(
                    name=cleaned_data.get("genre")
                )
                create_book = Book.objects.create(
                    title=new_book,
                    author=author,
                    book_cover=cleaned_data.get("book_cover"),
                )
                create_book.genre.add(genre)
                print(create_book)
                cleaned_data["book"] = create_book
                return cleaned_data
