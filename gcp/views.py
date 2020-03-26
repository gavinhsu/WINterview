from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class Speech_to_TextView(TemplateView):
    def get(self,request):
        click = print("hello")
        return render(request, "speech_to_text.html",{
            "click": click_button
        })
