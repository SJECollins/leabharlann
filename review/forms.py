from django import forms
from .models import MyBookReview


class MyBookReviewForm(forms.ModelForm):
    """
    Form for adding and editing book reviews.
    """

    class Meta:
        model = MyBookReview
        fields = ("book", "review", "rating", "private")
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 10}),
            "review": forms.Textarea(attrs={"rows": 5}),
        }
