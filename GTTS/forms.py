from django import forms

class UploadAnswersForm(forms.Form):  
  post = forms.CharField()