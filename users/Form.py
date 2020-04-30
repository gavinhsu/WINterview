from django import forms
class UserFrom(forms.Form):
    account = forms.CharField()
    password = forms.CharField()
