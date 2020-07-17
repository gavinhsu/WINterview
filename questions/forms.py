class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ["name", "videofile"]
