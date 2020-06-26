from django.conf.urls import url
from django.urls import path
#from django.contrib.auth.views import SpeechView
#import gtts.tests.test_tts.views
import GTTS.views 

app_name = 'GTTS'

urlpatterns = [
  path('', GTTS.views.QuesView.as_view()),
  path('', GTTS.views.UploadAnswersView.as_view()),
  #path(button_click, views.),
  
 ]