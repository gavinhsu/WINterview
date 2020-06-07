from django.conf.urls import url
from django.urls import path
#from django.contrib.auth.views import SpeechView
import gtts.tests.test_tts.views

app_name = 'GTTS'

urlpatterns = [
  path('speech_to_text/', GTTS.views.Speech),
  #path(button_click, views.),
  #path(r'^speech_to_text/$', Speech.as_view())
 ]