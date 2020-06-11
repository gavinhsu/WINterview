from django.shortcuts import render, redirect
from django.contrib import auth
import random
# from django.core.context_processors import csrf

from questions.models import Question

def showthis(request):
    max_id = Question.objects.order_by('-id')[0].id
    random_id = random.randint(1 , max_id)
    random_question = Question.objects.get(id=random_id)
    return render(request, 'speech_to_text.html', locals())