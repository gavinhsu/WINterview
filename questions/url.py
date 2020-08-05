from django.conf.urls import url
from django.urls import path
import questions.views

app_name = 'questions'

urlpatterns = [
  path('', questions.views.create)

  ]