from django.urls import path
import users.views

urlpatterns = [
  path('signUp/', users.views.signUp),
 ]
