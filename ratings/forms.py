from django import forms

from ratings.models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['review','rating']
        # widgets = {
        #     'rating': forms.SelectMultiple(),
        # }