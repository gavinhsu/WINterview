from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import path
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from GTTS.forms import UploadAnswersForm
from questions.models import Answer
from questions.models import Question
import random
#from django.core.context_processors import csrf


class QuesView(TemplateView):
    template_name = 'speech_to_text.html'
    
    def get(self, request):
        max_id = Question.objects.order_by('-id')[0].id
        random_id = random.randint(1 , max_id)
        random_question = Question.objects.get(id=random_id)
        return render(request, self.template_name, locals())


class UploadAnswersView(TemplateView):  
    template_name = 'speech_to_text.html' 
    
    def get(self, request):    
        form = UploadAnswersForm()    
        return render(request, self.template_name, {'form':form})

    def post(self, request):       
        form = UploadAnswersForm(request.POST) 

        if form.is_valid():      
            a1 = request.POST.get('a1','')  
            ans_obj = Answer(a1 = a1)
            ans_obj.save()
            return redirect()
        return render(request, self.template_name, {'form':form})