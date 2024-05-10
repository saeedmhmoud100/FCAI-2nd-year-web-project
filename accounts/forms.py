from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'}))
    is_admin = forms.BooleanField(required=False)