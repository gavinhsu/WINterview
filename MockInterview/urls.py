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
import GTTS.views
import nlp.views
#from GTTS.views import Speech
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', users.views.homepage),
    path('users/', include("users.url")),
    path('speech_to_text/', include("GTTS.url")),
    path('users/jobselect/speech_to_text/equipCheck', GTTS.views.equipCheck.as_view()),
    # nlp test
    path('nlp/', include('nlp.url'))
    # for unauthorized access dynamic translation
    # path('gtts/', include('gTTS.urls')),
    # # for user authorized dynamic translation
    # path('gtts_auth/', include('gTTS.urls_auth')),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
