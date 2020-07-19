from django.conf.urls import url
from django.urls import path
#from django.contrib.auth.views import SpeechView
#import gtts.tests.test_tts.views
import GTTS.views 

app_name = 'GTTS'

urlpatterns = [
  #path('equipCheck/', GTTS.views.equipCheck),
  path('', GTTS.views.QuesView.as_view()),
  path('reply2/', GTTS.views.QuesView2.as_view()),
  path('reply2/reply3/', GTTS.views.QuesView3.as_view()),
  path('reply2/reply3/reply4/', GTTS.views.QuesView4.as_view()),
  path('reply2/reply3/reply4/reply5/', GTTS.views.QuesView5.as_view()),
  #path('submit/', GTTS.views.UploadAnswersView.as_view()),
  # path('',GTTS.views.post)
  #path(button_click, views.),
  
 ]