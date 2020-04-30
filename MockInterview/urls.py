"""MockInterview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.jurls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
import users.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', users.views.homepage),
<<<<<<< HEAD
    path('users/', include('users.url')),
    #path('',include('users.url',namespace = 'users')),
    
=======
    path('users/', include("users.url")),
    path('speech_to_text/', include("SpeechText.url"))
>>>>>>> f97d17a40838b8ce779c516e6c99447974b7fa2d
]
