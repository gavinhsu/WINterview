from django.shortcuts import render, redirect
from django.contrib import auth
import random
# from django.views.decorators.csrf import csrf_protect
# from django.core.context_processors import csrf
from django.views.generic import TemplateView
from questions.models import *
from users.models import *
from users.models import Member
from GTTS.forms import UploadAnswersForm
from nlp.views import predict

def equipCheck(request):
    return render(request, 'equipCheck.html')


class QuesView(TemplateView):
    template_name = 'speech_to_text.html'

    def get(self, request):
      #print(request.session.session_key)

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      max_id = Software_Engineer.objects.latest('id').id
      random_ques_num = random.randint(1 , max_id)
      random_question = Software_Engineer.objects.get(QuesNum=random_ques_num)
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a1 = request.POST['note-textarea']
        
  
        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            # get Account instance from Member model SUPER IMPORTANT!!!
            account_instance = Member.objects.get(Account=account_name)
            print(account_instance)
            unit = Answer.objects.create(userID=account_instance)

        unit.a1 = a1
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
        print(uid)
        unit.save()

        # save result to Result models
        r1 = predict('a1')
        res = Result.objects.create(userID=account_instance, id=uid, r1=r1)
        res.save()

        return redirect('reply2/')

      
      return render(request, self.template_name,locals())   


class QuesView2(TemplateView):
    template_name = 'reply2.html'

    def get(self, request):
      #print(request.session.session_key)

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      max_id = Software_Engineer.objects.latest('id').id
      random_ques_num = random.randint(1 , max_id)
      random_question = Software_Engineer.objects.get(QuesNum=random_ques_num)
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a2 = request.POST['note-textarea']
  
        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            # get Account instance from Member model
            account_instance = Member.objects.get(Account=account_name)
            # retreive the user's id
            uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
            unit = Answer.objects.get(id=uid)
            print(unit)
            unit.a2 = a2

        unit.save()

        # save result to Result models
        r2 = predict('a2')
        res = Result.objects.get(id=uid)
        res.r2 = r2
        res.save()

        return redirect('reply3/')

      return render(request, self.template_name,locals())   


class QuesView3(TemplateView):
    template_name = 'reply3.html'

    def get(self, request):
      #print(request.session.session_key)

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      max_id = Software_Engineer.objects.latest('id').id
      random_ques_num = random.randint(1 , max_id)
      random_question = Software_Engineer.objects.get(QuesNum=random_ques_num)
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a3 = request.POST['note-textarea']
  
        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            # get Account instance from Member model
            account_instance = Member.objects.get(Account=account_name)
            # retreive the user's id
            uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
            unit = Answer.objects.get(id=uid)
            print(unit)
            unit.a3 = a3

        unit.save()

        # save result to Result models
        r3 = predict('a3')
        res = Result.objects.get(id=uid)
        res.r3 = r3
        res.save()

        return redirect('reply4/')

      return render(request, self.template_name,locals())  



# ---------------SAVE FOR FUTURE USE MAYBE-------------------------------------------------------
# class QuesView3(TemplateView):
#     template_name = 'reply3.html'

#     def get(self, request):
#       max_id = Software_Engineer.objects.latest('id').id
#       random_ques_num = random.randint(1 , max_id)
#       random_question = Software_Engineer.objects.get(QuesNum=random_ques_num)
#       return render(request, self.template_name, locals())
  
#     def post(self, request):     
#         if request.method == "POST":
#           a3 = request.POST['note-textarea']
#           uid = Answer.objects.all().order_by('-id')[0].id
#           unit = Answer.objects.get(id=uid)
#           unit.a3 = a3
#           unit.save()

#           r3 = predict('a3')
#           res = Result.objects.get(id=uid)
#           res.r3 = r3
#           res.save()
#           return redirect('reply4/')

#         return render(request, self.template_name, locals())  

        


