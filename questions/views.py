from django.shortcuts import render
# Create your views here.
from .models import Video
from .forms import *
from questions.models import *
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
# for news fetching
from newsapi import NewsApiClient

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
            form = DatabaseAdministratorForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')
        
        if 'NetworkEngineer' in request.POST:
            form = NetworkEngineerForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')
        
        if 'InvestmentBanking' in request.POST:
            form = InvestmentBankingForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')
        
        if 'SalesTrading' in request.POST:
            form = SalesTradingForm(request.POST)
            if form.is_valid():
                new = form.save()
                return HttpResponseRedirect('/ques/')

        if 'SalesTrading' in request.POST:
            form = SalesTradingForm(request.POST)
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



def newsfin(request):
    newsapi = NewsApiClient(api_key="a0f27104ee2a4586950818f8164ddce9")

    all_articles = newsapi.get_everything(domains='wsj.com', language='en')
    #top_headlines = newsapi.get_top_headlines(category='business',language='en',country='us')

    articles = all_articles['articles']

    desc = []
    news = []
    img = []
    url = []
    time = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        descript = str(myarticles['content']).split("…")[0]
        desc.append(descript + '...')
        print(myarticles['description'])
        img.append(myarticles['urlToImage'])
        url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ')
        p2 = p.replace('Z', ' ')
        time.append(p2)


    mylist = zip(news, desc, img, url, time)


    return render(request, 'newsfin.html', context={"mylist":mylist})



def news(request):
    newsapi = NewsApiClient(api_key="a0f27104ee2a4586950818f8164ddce9")

    # FINANCE news
    fin_news = newsapi.get_everything(domains='wsj.com', language='en')
    fin_articles = fin_news['articles']

    fin_desc = []
    fin_news = []
    fin_img = []
    fin_url = []
    fin_time = []

    for i in range(len(fin_articles)):
        myarticles = fin_articles[i]

        fin_news.append(myarticles['title'])
        fin_desc.append(myarticles['description'])
        fin_img.append(myarticles['urlToImage'])
        fin_url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ')
        p2 = p.replace('Z', ' ')
        fin_time.append(p2)

    fin_list = zip(fin_news, fin_desc, fin_img, fin_url, fin_time)

    # TECH news
    tech_news = newsapi.get_top_headlines(sources='techcrunch, the-verge')

    tech_articles = tech_news['articles']

    tech_desc = []
    tech_news = []
    tech_img = []
    tech_url = []
    tech_time = []

    for i in range(len(tech_articles)):
        myarticles = tech_articles[i]

        tech_news.append(myarticles['title'])
        tech_desc.append(myarticles['description'])
        tech_img.append(myarticles['urlToImage'])
        tech_url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ')
        p2 = p.replace('Z', ' ')
        tech_time.append(p2)

    tech_list = zip(tech_news, tech_desc, tech_img, tech_url, tech_time)

    # FINANCE news
    fin_news = newsapi.get_everything(domains='wsj.com', language='en')
    fin_articles = fin_news['articles']

    fin_desc = []
    fin_news = []
    fin_img = []
    fin_url = []
    fin_time = []

    for i in range(len(fin_articles)):
        myarticles = fin_articles[i]

        fin_news.append(myarticles['title'])
        fin_desc.append(myarticles['description'])
        fin_img.append(myarticles['urlToImage'])
        fin_url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ')
        p2 = p.replace('Z', ' ')
        fin_time.append(p2)

    fin_list = zip(fin_news, fin_desc, fin_img, fin_url, fin_time)


    return render(request, 'news.html', context={"tech_list":tech_list, "fin_list":fin_list})


    
