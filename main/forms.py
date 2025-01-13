from django import forms

class ShareForm(forms.Form):
    file = forms.FileField(label="File")
    accesspwd1 = forms.CharField(label="Protection password", widget=forms.PasswordInput, max_length=255)
    accesspwd2 = forms.CharField(label="Retype password", widget=forms.PasswordInput, max_length=255)
    deletionpwd1 = forms.CharField(label="Deletion password", widget=forms.PasswordInput, max_length=255)
    deletionpwd2 = forms.CharField(label="Retype password", widget=forms.PasswordInput, max_length=255)

class LoginForm(forms.Form):
    passwd = forms.CharField(label="Password", widget=forms.PasswordInput, max_length=255)
