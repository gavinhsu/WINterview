from django.conf.urls import url
from django.urls import path
#from django.contrib.auth.views import SpeechView
#import gtts.tests.test_tts.views
import GTTS.views 
import nlp.views

app_name = 'GTTS'

urlpatterns = [
  path('', GTTS.views.QuesView.as_view()),
  path('reply2/', GTTS.views.QuesView2.as_view()),
  path('reply2/reply3/', GTTS.views.QuesView3.as_view()),
  path('reply2/reply3/reply4/', GTTS.views.QuesView4.as_view()),
  path('reply2/reply3/reply4/reply5/', GTTS.views.QuesView5.as_view()),
  path('reply2/reply3/reply4/reply5/reply6/', GTTS.views.QuesView6.as_view()),
  path('reply2/reply3/reply4/reply5/reply6/reply7/', GTTS.views.QuesView7.as_view()),
  path('reply2/reply3/reply4/reply5/reply6/reply7/reply8/', GTTS.views.QuesView8.as_view()),
  path('reply2/reply3/reply4/reply5/reply6/reply7/reply8/reply9/', GTTS.views.QuesView9.as_view()),
  path('reply2/reply3/reply4/reply5/reply6/reply7/reply8/reply9/reply10/', GTTS.views.QuesView10.as_view()),
  path('reply2/reply3/reply4/reply5/reply6/reply7/reply8/reply9/reply10/result/', nlp.views.ResultView.as_view()),

  
 ]