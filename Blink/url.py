from django.conf.urls import url
from django.urls import path
#from django.contrib.auth.views import SpeechView
#import gtts.tests.test_tts.views
import Blink.views 

app_name = 'Blink'

urlpatterns = [
  path('', Blink.views.AjaxSaveAudio.as_view())

 ]