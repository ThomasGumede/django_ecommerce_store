from django import forms
from products.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'text', 'rating']

        # widgets = {
        #     'text': forms.Textarea(),
        #     'rating': forms.RadioSelect
        # }