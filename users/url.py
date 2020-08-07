from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView
import users.views
from users.views import logout

app_name = 'users'

urlpatterns = [
  #path('login/',LoginView.as_view(template_name='users/login.html'),name = "login"),
  path('signUp/', users.views.signUp),
  path('regist/', users.views.regist),

  path('login/', users.views.login),
  path('jobselect/',users.views.jobselect),
  #path('jobselect/speech_to_text/equipCheck', users.views.equipCheck),
  #path('users/logout/', logout)
  path('logout/',users.views.logout),
  path('aboutUs/',users.views.aboutUs),
  path('services/',users.views.services),
  path('team/',users.views.services),
  path('questionBank/',users.views.questionBank),
  path('interviewSkill/',users.views.interviewSkill),
  path('companyProfile/',users.views.companyProfile),
  path('News/',users.views.News),
  path('contactUs/',users.views.contactUs),
 ]
