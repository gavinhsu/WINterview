from django.shortcuts import render, redirect
from django.contrib import auth
import random
# from django.views.decorators.csrf import csrf_protect
# from django.core.context_processors import csrf

from django.views.generic import TemplateView
from questions.models import *
from GTTS.forms import UploadAnswersForm
from nlp.views import predict

def equipCheck(request):
    return render(request, 'equipCheck.html')


class QuesView(TemplateView):
    template_name = 'speech_to_text.html'

    # def __init__(self, init_args):
    #     self.uid = Answer.objects.all().order_by('-id')[0].id

    # def get_uid(self):
    #   return self.uid

    # def set_uid(self, val):
    #   uid = x

    def get(self, request):
      max_id = Software_Engineer.objects.latest('id').id
      random_ques_num = random.randint(1 , max_id)
      random_question = Software_Engineer.objects.get(QuesNum=random_ques_num)
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a1 = request.POST['note-textarea']
        #unit = Answer.objects.create(a1=a1)
        unit = Answer.objects.get(id=59)
        unit.a1 = a1
        # retreive the latest id
        uid = Answer.objects.all().order_by('-id')[0].id
        unit.save()

        # save result to Result models
        r1 = predict('a1')
        res = Result.objects.create(id=uid, r1=r1)
        res.save()

        return redirect('reply2/')

      
      return render(request, self.template_name,locals())   


class QuesView2(TemplateView):
    template_name = 'reply2.html'

    # def __init__(self):
    #     uid = QuesView.get_uid(QuesView)
    #     A = QuesView(init_args=uid)
    #     #uid = QuesView.get_uid()

    def get(self, request):
      max_id = Software_Engineer.objects.latest('id').id
      random_ques_num = random.randint(1 , max_id)
      random_question = Software_Engineer.objects.get(QuesNum=random_ques_num)
      return render(request, self.template_name, locals())
  
    def post(self, request):     
        if request.method == "POST":
          a2 = request.POST['note-textarea']
          uid = Answer.objects.all().order_by('-id')[0].id
          unit = Answer.objects.get(id=uid)
          unit.a2 = a2
          unit.save()

          r2 = predict('a2')
          res = Result.objects.get(id=uid)
          res.r2 = r2
          res.save()
          return redirect('reply3/')

        return render(request, self.template_name, locals())  


class QuesView3(TemplateView):
    template_name = 'reply3.html'

    # def __init__(self):
    #     uid = QuesView.get_uid(QuesView)
    #     A = QuesView(init_args=uid)
    #     #uid = QuesView.get_uid()

    def get(self, request):
      max_id = Software_Engineer.objects.latest('id').id
      random_ques_num = random.randint(1 , max_id)
      random_question = Software_Engineer.objects.get(QuesNum=random_ques_num)
      return render(request, self.template_name, locals())
  
    def post(self, request):     
        if request.method == "POST":
          a3 = request.POST['note-textarea']
          uid = Answer.objects.all().order_by('-id')[0].id
          unit = Answer.objects.get(id=uid)
          unit.a3 = a3
          unit.save()

          r3 = predict('a3')
          res = Result.objects.get(id=uid)
          res.r3 = r3
          res.save()
          return redirect('reply4/')

        return render(request, self.template_name, locals())  


