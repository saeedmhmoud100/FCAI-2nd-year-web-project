from django import forms

from books.models import Book


class CreateBookForm(forms.ModelForm):

    title = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder': 'Enter the book title'}))
    author = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder': 'Enter the book author'}))
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True,widget=forms.NumberInput(attrs={'placeholder': 'Enter the book price'}))
    description = forms.CharField(max_length=500, required=True,widget=forms.Textarea(attrs={'placeholder': 'Enter the book description'}))
    image = forms.FileField(required=True,widget=forms.FileInput(attrs={'placeholder': 'Upload the book image'}))
    class Meta:
        model = Book
        fields = ('title', 'author', 'price', 'category', 'description', 'image')

class UpdateBookForm(forms.ModelForm):

    title = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder': 'Enter the book title'}))
    author = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder': 'Enter the book author'}))
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True,widget=forms.NumberInput(attrs={'placeholder': 'Enter the book price'}))
    description = forms.CharField(max_length=500, required=True,widget=forms.Textarea(attrs={'placeholder': 'Enter the book description'}))
    image = forms.FileField(required=False,widget=forms.FileInput(attrs={'placeholder': 'Upload the book image'}))
    class Meta:
        model = Book
        fields = ('title', 'author', 'price', 'category', 'description', 'image','borrower')