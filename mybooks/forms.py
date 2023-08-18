from django import forms
from books.models import Author, Book, Genre

from .models import MyBook


class MyBookForm(forms.ModelForm):
    """
    ModelForm for the MyBook model.
    Allows the user to add a book to their shelf.
    Extra fields are new_book, author_first, author_last, genre, book_cover.
    Can be used to add a new book to the database.
    """

    new_book = forms.CharField(max_length=140, required=False)
    author_first = forms.CharField(max_length=100, required=False)
    author_last = forms.CharField(max_length=100, required=False)
    genre = forms.CharField(max_length=100, required=False)
    book_cover = forms.ImageField(required=False)

    class Meta:
        model = MyBook
        fields = [
            "book",
            "summary",
            "unread",
            "pages_total",
            "pages_read",
            "started_reading_on",
            "currently_reading",
            "finished",
            "finished_reading_on",
            "notes",
            "favourite",
            "private",
        ]
        widgets = {
            "started_reading_on": forms.DateInput(attrs={"type": "date"}),
            "finished_reading_on": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(MyBookForm, self).__init__(*args, **kwargs)
        self.fields["book"].required = False
        self.fields["new_book"].label = "Book title"
        self.fields["author_first"].label = "Author first name"
        self.fields["author_last"].label = "Author last name"
        self.fields["genre"].label = "Genre"
        self.fields["book_cover"].label = "Book cover"

    def clean(self):
        cleaned_data = super(MyBookForm, self).clean()
        existing_book = cleaned_data.get("book")
        new_book = cleaned_data.get("new_book")
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
                genre, created = Genre.objects.get_or_create(
                    name=cleaned_data.get("genre")
                )
                create_book = Book.objects.create(
                    title=new_book,
                    author=author,
                    book_cover=cleaned_data.get("book_cover"),
                )
                create_book.genre.add(genre)
                cleaned_data["book"] = create_book
                return cleaned_data


class MyBookEditForm(forms.ModelForm):
    """
    ModelForm to edit the MyBook model.
    """

    add_genre = forms.CharField(max_length=100, required=False)

    class Meta:
        model = MyBook
        fields = [
            "book",
            "summary",
            "unread",
            "pages_total",
            "pages_read",
            "started_reading_on",
            "currently_reading",
            "finished",
            "finished_reading_on",
            "notes",
            "favourite",
            "private",
        ]
        widgets = {
            "started_reading_on": forms.DateInput(attrs={"type": "date"}),
            "finished_reading_on": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(MyBookEditForm, self).__init__(*args, **kwargs)
        self.fields["book"].disabled = True


class MyBookStartForm(forms.ModelForm):
    """
    ModelForm to mark a book as currently reading.
    """

    class Meta:
        model = MyBook
        fields = ["started_reading_on"]
        widgets = {"started_reading_on": forms.DateInput(attrs={"type": "date"})}


class MyBookProgressForm(forms.ModelForm):
    """
    ModelForm to update the progress of a book.
    """

    class Meta:
        model = MyBook
        fields = ["pages_read"]


class MyBookFinishedForm(forms.ModelForm):
    """
    ModelForm to mark a book as finished.
    """

    class Meta:
        model = MyBook
        fields = ["finished_reading_on"]
        widgets = {"finished_reading_on": forms.DateInput(attrs={"type": "date"})}


class MyBookSummaryForm(forms.ModelForm):
    """
    ModelForm to add a summary to a book.
    """

    class Meta:
        model = MyBook
        fields = ["summary"]


class MyBookNotesForm(forms.ModelForm):
    """
    ModelForm to add notes to a book.
    """

    class Meta:
        model = MyBook
        fields = ["notes"]
