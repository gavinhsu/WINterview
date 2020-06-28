from django import forms

class UploadAnswersForm(forms.Form):  
  answer_note = forms.CharField(label = 'Your Answer', widget=forms.Textarea(
    attrs={'placeholder':"Your answer will be shown here.", 'class':'answerNote'}
  ))

  # def cleaan(self):
  #   cleaned_data = super(UploadAnswersForm, self).clean()
  #   answer_note = cleaned_data.get('answer_note')
  #   if not answer_note:
  #     raise forms.ValidationError('Please answer the question!')
  # class Media:
  #   js = ('js/speech_to_text.js')