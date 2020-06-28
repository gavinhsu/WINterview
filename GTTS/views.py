from django.shortcuts import render, redirect
from django.contrib import auth
import random
# from django.views.decorators.csrf import csrf_protect
# from django.core.context_processors import csrf

from django.views.generic import TemplateView
from questions.models import Question
from questions.models import Answer
from GTTS.forms import UploadAnswersForm


class QuesView(TemplateView):
    template_name = 'speech_to_text.html'

    def get(self, request):
        max_id = Question.objects.order_by('-id')[0].id
        random_id = random.randint(1 , max_id)
        random_question = Question.objects.get(id=random_id)
        return render(request, self.template_name, locals())



def post(request):     
  if request.method == "POST":
    a1 = request.POST['note-textarea']
    unit = Answer.objects.create(a1=a1)
    unit.save()
    return redirect('/speech_to_text/')
  else:
    mess = "Please answer the question!"
  print(request)

  return render(request, 'speech_to_text.html',locals())   