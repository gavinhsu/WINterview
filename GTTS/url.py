from django.conf.urls import url
from django.urls import path
#from django.contrib.auth.views import SpeechView
#import gtts.tests.test_tts.views
import GTTS.views 

app_name = 'GTTS'

urlpatterns = [
  path('', GTTS.views.QuesView.as_view()),
  path('speech_to_text/reply2/', GTTS.views.QuesView2.as_view()),
  #path('submit/', GTTS.views.UploadAnswersView.as_view()),
  # path('',GTTS.views.post)
  #path(button_click, views.),
  
 ]