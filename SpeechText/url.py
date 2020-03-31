from django.urls import path
import TextSpeech.views

path('speech_to_text/', SpeechText.HelloViews.View.as_view()),
