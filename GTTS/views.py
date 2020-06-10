from django.shortcuts import render, redirect
from django.contrib import auth
# from django.core.context_processors import csrf

from questions.models import Question

def showthis(request):
    questions= Question.objects.all()

    return render(request, 'speech_to_text.html', {'questions': questions})