from django.shortcuts import render, redirect
from django.contrib import auth
import random
# from django.views.decorators.csrf import csrf_protect
# from django.core.context_processors import csrf

from django.views.generic import TemplateView
from questions.models import *
from GTTS.forms import UploadAnswersForm


class QuesView(TemplateView):
    template_name = 'speech_to_text.html'



    def get(self, request):
      max_id = Software_Engineer.objects.latest('id').id
      random_ques_num = random.randint(1 , max_id)
      random_question = Software_Engineer.objects.get(QuesNum=random_ques_num)
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        a1 = request.POST['note-textarea']
        unit = Answer.objects.create(a1=a1)
        unit.save()
        return redirect('speech_to_text/reply2/')

      return render(request, self.template_name,locals())   


class QuesView2(TemplateView):
    template_name = 'reply2.html'

    def get(self, request):
      max_id = Software_Engineer.objects.latest('id').id
      random_ques_num = random.randint(1 , max_id)
      random_question = Software_Engineer.objects.get(QuesNum=random_ques_num)
      return render(request, self.template_name, locals())
  
    def post(self, request):     
        if request.method == "POST":
          a2 = request.POST['note-textarea']
          unit = Answer.objects.create(a2=a2)
          unit.save()
          return redirect('speech_to_text/reply3/')

        return render(request, self.template_name,locals())  

