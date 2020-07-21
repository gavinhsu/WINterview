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



class equipCheck(TemplateView):
  template_name = 'equipCheck.html'

  def __init__(self, job_name=None):
    self.job_name = job_name

  def get(self, request):
    job_name = request.session['job_name']
    self.job_name = job_name
    print(job_name)

    def create_ques(job):
      # create random question
      # max_id = job.objects.latest('id').id
      # num_list = list(range(1, max_id+1))
      # random.shuffle(num_list)

      # rand_list = []
      # global ques_list
      # ques_list = []

      # # output 6 questions for now, ADD MORE IN FUTURE
      # for num in range(6):
      #   num = num_list.pop()
      #   rand_list.append(num)

      #   question = job.objects.filter(id=num).values('Ques')
      #   for ques in question:
      #     ques = ques['Ques']
      #     ques_list.append(ques)

      # print(ques_list)
      # print(rand_list)


      # EASY
      easy_QS = job.objects.filter(Difficulties='easy').values('Ques')
      easy_list = []
      for ques in easy_QS:
        ques = ques["Ques"]
        easy_list.append(ques)

      easy_length = len(easy_list)
      easy_rand = random.sample(easy_list, 2)
      # global r1
      # global r2
      global r1
      global r2
      r1 = easy_rand[0]
      r2 = easy_rand[1]

      # MEDIUM
      medium_QS = job.objects.filter(Difficulties='medium').values('Ques')
      medium_list = []
      for ques in medium_QS:
        ques = ques["Ques"]
        medium_list.append(ques)

      medium_length = len(medium_list)
      medium_rand = random.sample(medium_list, 2)
      global r3
      global r4
      r3 = medium_rand[0]
      r4 = medium_rand[1]      

      # HARD
      hard_QS = job.objects.filter(Difficulties='hard').values('Ques')
      hard_list = []
      for ques in hard_QS:
        ques = ques["Ques"]
        hard_list.append(ques)

      hard_length = len(hard_list)
      hard_rand = random.sample(hard_list, 2)
      global r5
      global r6
      r5 = hard_rand[0]
      r6 = hard_rand[1]    


    # throw questions according to selected job ==> ADD JOBS IN FUTURE!!
    if job_name == 'Software Engineer':
      create_ques(Software_Engineer)
    elif job_name == 'Cashier':
      create_ques(Venture_Capital)
    else:
      print('Job questions not created yet!!!')

    final_list = [r1,r2,r3,r4,r5,r6]
    rand_final_list = random.shuffle(final_list)
    print(rand_final_list)

    global q1
    global q2
    global q3
    global q4
    global q5
    global q6
    q1 = final_list[0]
    q2 = final_list[1]
    q3 = final_list[2]
    q4 = final_list[3]
    q5 = final_list[4]
    q6 = final_list[5]


    return render(request, self.template_name)



class QuesView(TemplateView):
    template_name = 'speech_to_text.html'

    def __init__(self, job_name=None):
      self.job_name = job_name

    def get(self, request):
      job_name = request.session['job_name']
      self.job_name = job_name
      #print(self.job_name)

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q1
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

      random_question = q2
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

      random_question = q3
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
            unit.a3 = a3

        unit.save()

        # save result to Result models
        r3 = predict('a3')
        res = Result.objects.get(id=uid)
        res.r3 = r3
        res.save()

        return redirect('reply4/')

      return render(request, self.template_name,locals())  

class QuesView4(TemplateView):
    template_name = 'reply4.html'

    def get(self, request):
      #print(request.session.session_key)

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q4
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a4 = request.POST['note-textarea']
  
        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            # get Account instance from Member model
            account_instance = Member.objects.get(Account=account_name)
            # retreive the user's id
            uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
            unit = Answer.objects.get(id=uid)
            unit.a4 = a4

        unit.save()

        # save result to Result models
        r4 = predict('a4')
        res = Result.objects.get(id=uid)
        res.r4 = r4
        res.save()

        return redirect('reply5/')

      return render(request, self.template_name,locals())  

class QuesView5(TemplateView):
    template_name = 'reply5.html'

    def get(self, request):
      #print(request.session.session_key)

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q5
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a4 = request.POST['note-textarea']
  
        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            # get Account instance from Member model
            account_instance = Member.objects.get(Account=account_name)
            # retreive the user's id
            uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
            unit = Answer.objects.get(id=uid)
            unit.a5 = a5

        unit.save()

        # save result to Result models
        r5 = predict('a5')
        res = Result.objects.get(id=uid)
        res.r5 = r5
        res.save()

        return redirect('reply6/')

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

        


