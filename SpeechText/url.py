from django.urls import path
import TextSpeech.views

urlpatterns = [
    path('speech_to_text/', SpeechText.HelloViews.View.as_view()),
    
]
