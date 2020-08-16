from django.shortcuts import render
# Create your views here.
from .models import Video
from .forms import *
from questions.models import *
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

def create(request):
    if request.method == 'POST':
        if 'SoftwareEngineer' in request.POST:
            form = SoftwareEngineerForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')

        if 'DataScientist' in request.POST:
            form = DataScientistForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')
        if 'DatabaseAdministrator' in request.POST:
            form = DataScientistForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')
        
        if 'NetworkEngineer' in request.POST:
            form = DataScientistForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')
        
        if 'InvestmentBanking' in request.POST:
            form = DataScientistForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')
        
        if 'SalesTrading' in request.POST:
            form = DataScientistForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')

        if 'SalesTrading' in request.POST:
            form = DataScientistForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')

        if 'Research' in request.POST:
            form = ResearchForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')
        
        if 'QuantitativeTrading' in request.POST:
            form = QuantitativeTradingForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')

        if 'Venture_Capital' in request.POST:
            form = Venture_CapitalForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')

    form1 = SoftwareEngineerForm()
    form2 = DataScientistForm()
    form3 = DatabaseAdministratorForm()
    form4 = NetworkEngineerForm()
    form5 = InvestmentBankingForm()
    form6 = SalesTradingForm()
    form7 = ResearchForm()
    form8 = QuantitativeTradingForm()
    form9 = Venture_CapitalForm()

    return render(request, 'throwQues.html', {
        'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5, 
        'form6': form6, 'form7': form7, 'form8': form8, 'form9': form9})

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
