from django.shortcuts import render
from questions.models import Question
# Create your views here.
from django.shortcuts import render
from .models import Video
from .forms import VideoForm

def showvideo(request):

    lastvideo= Video.objects.last()

    videofile= lastvideo.videofile


    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()


    context= {'videofile': videofile,
              'form': form
              }


    return render(request, 'Blog/videos.html', context)
