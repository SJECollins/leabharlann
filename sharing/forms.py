from django import forms

from .models import ShareBook, ShareBookRequest


class ShareBookLoanerForm(forms.ModelForm):
    class Meta:
        model = ShareBook
        fields = [
            "shelf_book",
            "book",
            "borrower",
            "borrower_alt",
            "date_shared",
            "notes",
        ]
        widgets = {
            "date_shared": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super(ShareBookLoanerForm, self).clean()
        borrower = cleaned_data.get("borrower")
        borrower_alt = cleaned_data.get("borrower_alt")
        if borrower and borrower_alt:
            raise forms.ValidationError("You can't select a user and enter a name")
        if not borrower and not borrower_alt:
            raise forms.ValidationError("You must select a user or enter a name")
        return cleaned_data


class ShareBookBorrowerForm(forms.ModelForm):
    class Meta:
        model = ShareBook
        fields = [
            "shelf_book",
            "book",
            "date_shared",
            "notes",
        ]
        widgets = {
            "date_shared": forms.DateInput(attrs={"type": "date"}),
        }


class ShareBookReturnForm(forms.ModelForm):
    class Meta:
        model = ShareBook
        fields = ["returned", "date_returned", "notes"]
        widgets = {
            "date_returned": forms.DateInput(attrs={"type": "date"}),
        }


class ShareBookRequestForm(forms.ModelForm):
    class Meta:
        model = ShareBookRequest
        fields = ["shelf_book", "book", "borrower"]


class ShareBookRequestAcceptForm(forms.ModelForm):
    class Meta:
        model = ShareBookRequest
        fields = ["accepted"]


class ShareBookRequestRejectForm(forms.ModelForm):
    class Meta:
        model = ShareBookRequest
        fields = ["rejected", "reject_reason"]
