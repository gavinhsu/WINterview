from django.urls import path
import gcp.views

path('speech_to_text/', gcp.HelloViews.View.as_view()),
