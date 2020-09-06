from django.shortcuts import render, redirect
from django.contrib import auth
import random
import base64
from MockInterview.settings import BASE_DIR
import os, re, string
# from django.views.decorators.csrf import csrf_protect
# from django.core.context_processors import csrf
from django.views.generic import TemplateView
from questions.models import *
from questions.forms import *
from users.models import *
from users.models import Member
from GTTS.forms import UploadAnswersForm
from nlp.views import predict
from Blink.tasks import *
from django.core.files import File
from Emotion.views import *


# TEST get base64 ###############################################

# decode from base64 to mp4 file
# unit = Answer.objects.get(id=199)
# text = unit.a1
# text = text[23:]
# fh = open("test_vid.mp4", "wb")
# fh.write(base64.b64decode(text))
# fh.close()
# print('VIDEO DECODED')

# # save to django model
# f = open('test_vid.mp4', 'rb')
# vid_unit = Video.objects.get(id=7)
# vid_unit.videofile.save('test_vid.mp4', File(f), True)
# f.close()
# print('VIDEO SAVED TO MODEL')

# # retrieve video file
# vid_instance = Video.objects.get(id=7).videofile 
# vid_instance = str(vid_instance)
# vidname = str(vid_instance[7:])
# print(vidname)
# vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
# blink(vid_path)



class equipCheck(TemplateView): 
  template_name = 'equipCheck.html'

  def __init__(self, job_name=None):
    self.job_name = job_name

  def get(self, request):
    job_name = request.session['job_name']
    self.job_name = job_name
    print('You selected: '+ job_name)

    def create_ques(job):

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
      global r1, r2
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
      global r3, r4
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
      global r5, r6
      r5 = hard_rand[0]
      r6 = hard_rand[1]

      global final_list
      final_list = [r1,r2,r3,r4,r5,r6]
      random.shuffle(final_list)

      # get difficulty of questions
      global diff_list
      diff_list = []
      for r in final_list:
        diff_QS = job.objects.filter(Ques=r).values('Difficulties')
        for diff in diff_QS:
          diff = diff['Difficulties']
          diff_list.append(diff)
    

    # throw questions according to selected job ==> ADD JOBS IN FUTURE!!
    if job_name == 'Software Engineer':
      create_ques(Software_Engineer)
    # for testing purposes only
    elif job_name == 'Cashier':
      create_ques(Test_Job_pls_dont_add_shit_into_this_model_thank)
    elif job_name == 'Sales Trading':
      create_ques(Sales_Trading)
    elif job_name == 'Hardware Engineer':
      create_ques(Hardware_Engineer)
    elif job_name == 'ML Engineer':
      create_ques(ML_Engineer)
    elif job_name == 'MIS':
      create_ques(MIS)
    elif job_name == 'Audit':
      create_ques(Audit)
    elif job_name == 'Quantitative':
      create_ques(Quantitative)
    elif job_name == 'Research':
      create_ques(Research)
    elif job_name == 'Investment Banking':
      create_ques(Investment_Banking)
    elif job_name == 'Data Scientist':
      create_ques(Data_Scientist)
    else:
      print('Job questions not created yet!!!')


    global q1,q2,q3,q4,q5,q6
    q1 = final_list[0]
    q2 = final_list[1]
    q3 = final_list[2]
    q4 = final_list[3]
    q5 = final_list[4]
    q6 = final_list[5]

    # apply different time for different difficulty
    global prepare_time
    global answer_time
    prepare_time = []
    answer_time = []
    for i in range(0,6):
      if diff_list[i] == 'easy':
        prepare_time.append(10)
        answer_time.append(30)
      elif diff_list[i] == 'medium':
        prepare_time.append(10)
        answer_time.append(30)
      else:
        prepare_time.append(10)
        answer_time.append(30)

    print(diff_list)
    print(prepare_time)
    print(answer_time)

    global time_dict
    time_dict = {}
    for x in range(0,6):
      time_dict["prep_time{0}".format(x+1)] = prepare_time[x]
      time_dict["ans_time{0}".format(x+1)] = answer_time[x]
    
    return render(request, self.template_name)



class QuesView(TemplateView):
    template_name = 'speech_to_text.html'

    def __init__(self, job_name=None):
      self.job_name = job_name

    def get(self, request):
      
      job_name = request.session['job_name']
      self.job_name = job_name

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)
            # create answer & result table when getting website
            unit = Answer.objects.create(userID=account_instance, selected_job=job_name)
            uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
            res = Result.objects.create(userID=account_instance, id=uid)
            # create video table when getting website
            vid_unit = Video.objects.create(userID=account_instance, id=uid)
            vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')

      random_question = q1
      prep_time1 = time_dict['prep_time1']
      ans_time1 = time_dict['ans_time1']
      total_time1 = prep_time1 + ans_time1 - 5

      
      return render(request, self.template_name, locals())
        
    def post(self, request):
      if request.method == "POST":
        # save answer to Answer models
        a1 = request.POST['note-textarea']
        v1 = request.POST['video']

        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)        
        
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')   
        unit = Answer.objects.get(id=uid)
        unit.a1 = a1
        unit.v1 = v1
        unit.save()

        # retrieve video instance
        vid_unit = Video.objects.get(userID=account_instance, id=uid)
        vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')  
        

        # save result to Result models
        # r1 = predict('a1')
        # res = Result.objects.get(id=uid)
        # res.r1 = r1
        # res.save()

        # decode base64 to mp4 file
        text = unit.v1
        text = text[23:]
        fh = open('interview_vid.mp4', 'wb')
        fh.write(base64.b64decode(text))
        fh.close()
        print('VIDEO DECODED!', '\n')

        # save to django video model
        f = open('interview_vid.mp4', 'rb')
        vid_unit.vid1.save('interview_vid.mp4', File(f), True)
        f.close()
        print('VIDEO SAVED TO MODEL!', '\n')

        # retrieve video file from django model
        vid_instance = Video.objects.get(id=uid).vid1
        print(vid_instance)
        vid_instance = str(vid_instance)
        vidname = str(vid_instance[7:])
        print(vidname)
        vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
        
        # do blink detection and save to Result model
        blink1(vid_path, account_name)
        emotion(vid_path, account_name)

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
      prep_time2 = time_dict['prep_time2']
      ans_time2 = time_dict['ans_time2']
      total_time2 = prep_time2 + ans_time2 - 5

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

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q3
      prep_time3 = time_dict['prep_time3']
      ans_time3 = time_dict['ans_time3']
      total_time3 = prep_time3 + ans_time3
      
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
      prep_time4 = time_dict['prep_time4']
      ans_time4 = time_dict['ans_time4']
      total_time4 = prep_time4 + ans_time4
      
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
      prep_time5 = time_dict['prep_time5']
      ans_time5 = time_dict['ans_time5']
      total_time5 = prep_time5 + ans_time5
      
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a5 = request.POST['note-textarea']
  
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


class QuesView6(TemplateView):
    template_name = 'reply6.html'

    def get(self, request):
      #print(request.session.session_key)

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q6
      prep_time6 = time_dict['prep_time6']
      ans_time6 = time_dict['ans_time6']
      total_time6 = prep_time6 + ans_time6
      
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a6 = request.POST['note-textarea']
  
        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            # get Account instance from Member model
            account_instance = Member.objects.get(Account=account_name)
            # retreive the user's id
            uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
            unit = Answer.objects.get(id=uid)
            unit.a6 = a6

        unit.save()

        # save result to Result models
        r6 = predict('a6')
        res = Result.objects.get(id=uid)
        res.r6 = r6
        res.save()

        return redirect('reply7/')

      return render(request, self.template_name,locals()) 

        


