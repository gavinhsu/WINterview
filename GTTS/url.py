from django.conf.urls import url
from django.urls import path
#from django.contrib.auth.views import SpeechView
import GTTS.views

app_name = 'GTTS'

urlpatterns = [
  path('speech_to_text/', GTTS.views.Speech),
 ]