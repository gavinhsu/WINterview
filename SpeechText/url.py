from django.urls import path
import SpeechText.views

urlpatterns = [
    path('test/', SpeechText.views.speechView.as_view()),
    path('', SpeechText.views.speechView.as_view()),
]
