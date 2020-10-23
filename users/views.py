from django.shortcuts import render
#from django.views.generic import TemplateViews
from users.models import Member
from questions.models import Result, Answer
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect

from django.views.decorators.csrf import csrf_exempt
from . import Form,models
from django.contrib import auth
# for news fetching
from newsapi import NewsApiClient
import requests
from django.views.generic import TemplateView
import pandas as pd
# import django_tables2 as tables


def homepage(request):
    return render(request, 'homepage.html')

def signUp(request):
    return render(request, 'signUp.html')

def aboutUs(request):
    return render(request, 'aboutUs.html')

def services(request):
    return render(request,'services.html')

class personalFile(TemplateView):
    template_name = 'personalFile.html'

    def get(self, request):
        account_name = request.session['account']       
        job_name = request.session['job_name']
        self.account_name = account_name
        self.job_name = job_name

        # get the entire result table 
        account_instance = Member.objects.get(Account=account_name)
        res_id = Result.objects.filter(userID=account_instance).order_by('-id')[:1].values('id') 

        name_list = []
        job_list = []
        date_list = []
        time_list = []
        
        for item in Result.objects.all():
            name_list.append(item.userID)
            job_list.append(item.selected_job)
            date_list.append(item.created_date)
            time_list.append(str(item.created_time)[:5])
        num_list = list(range(1, len(name_list)+1))
        
        df = pd.DataFrame({'Name':name_list, 'SelectedJob':job_list, 'Date':date_list, 'Time':time_list, 'ID':num_list})

        return render(request, self.template_name, locals())


def questionBank(request):
    return render(request,'questionBank.html')

def interviewSkill(request):
    return render(request,'interviewSkill.html')

def companyProfile(request):

    # job news for tech---------------------------------------------------------------
    newsapi = NewsApiClient(api_key="16c7fedbd9e44985909000cfc198020a")

    # Intel news
    intel_news = newsapi.get_everything(q='intel',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      language='en',)

    intel_articles = intel_news['articles']

    intel_desc = []
    intel_news = []
    intel_url = []
    intel_time = []

    for i in range(3):
        myarticles = intel_articles[i]

        intel_news.append(myarticles['title'])
        intel_desc.append(myarticles['description'])
        intel_url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ').replace('Z', ' ')
        intel_time.append(p)

    intel_list = zip(intel_news, intel_desc, intel_url, intel_time)

    # Microsoft news
    microsoft_news = newsapi.get_everything(q='microsoft',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      language='en',)

    microsoft_articles = microsoft_news['articles']

    microsoft_desc = []
    microsoft_news = []
    microsoft_url = []
    microsoft_time = []

    for i in range(3):
        myarticles = microsoft_articles[i]

        microsoft_news.append(myarticles['title'])
        microsoft_desc.append(myarticles['description'])
        microsoft_url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ').replace('Z', ' ')
        microsoft_time.append(p)

    microsoft_list = zip(microsoft_news, microsoft_desc, microsoft_url, microsoft_time)


    # Google news
    google_news = newsapi.get_everything(q='google',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      language='en',)

    google_articles = google_news['articles']

    google_desc = []
    google_news = []
    google_url = []
    google_time = []

    for i in range(3):
        myarticles = google_articles[i]

        google_news.append(myarticles['title'])
        google_desc.append(myarticles['description'])
        google_url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ').replace('Z', ' ')
        google_time.append(p)

    google_list = zip(google_news, google_desc, google_url, google_time)


    # IBM news
    IBM_news = newsapi.get_everything(q='IBM',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      language='en',)

    IBM_articles = IBM_news['articles']

    IBM_desc = []
    IBM_news = []
    IBM_url = []
    IBM_time = []

    for i in range(3):
        myarticles = IBM_articles[i]

        IBM_news.append(myarticles['title'])
        IBM_desc.append(myarticles['description'])
        IBM_url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ').replace('Z', ' ')
        IBM_time.append(p)

    IBM_list = zip(IBM_news, IBM_desc, IBM_url, IBM_time)


    # TSMC news
    TSMC_news = newsapi.get_everything(q='TSMC',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      language='en',)

    TSMC_articles = TSMC_news['articles']

    TSMC_desc = []
    TSMC_news = []
    TSMC_url = []
    TSMC_time = []

    #temporarily no news
    for i in range(1):
        myarticles = TSMC_articles[i]
        TSMC_news.append(myarticles['title'])
        TSMC_desc.append(myarticles['description'])
        TSMC_url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ').replace('Z', ' ')
        TSMC_time.append(p)

    TSMC_list = zip(TSMC_news, TSMC_desc, TSMC_url, TSMC_time)


    # morgan news
    morgan_news = newsapi.get_everything(q='morgan',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      language='en',)

    morgan_articles = morgan_news['articles']

    morgan_desc = []
    morgan_news = []
    morgan_url = []
    morgan_time = []

    for i in range(3):
        myarticles = morgan_articles[i]

        morgan_news.append(myarticles['title'])
        morgan_desc.append(myarticles['description'])
        morgan_url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ').replace('Z', ' ')
        morgan_time.append(p)

    morgan_list = zip(morgan_news, morgan_desc, morgan_url, morgan_time)

    # hsbc news
    hsbc_news = newsapi.get_everything(q='hsbc',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      language='en',)

    hsbc_articles = hsbc_news['articles']

    hsbc_desc = []
    hsbc_news = []
    hsbc_url = []
    hsbc_time = []

    for i in range(3):
        myarticles = hsbc_articles[i]

        hsbc_news.append(myarticles['title'])
        hsbc_desc.append(myarticles['description'])
        hsbc_url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ').replace('Z', ' ')
        hsbc_time.append(p)

    hsbc_list = zip(hsbc_news, hsbc_desc, hsbc_url, hsbc_time)

    # Citigroup news
    # citigroup_news = newsapi.get_everything(q='Citi',
    #                                   sources='bbc-news,the-verge, ',
    #                                   domains='bbc.co.uk,techcrunch.com',
    #                                   language='en',)

    # citigroup_articles = citigroup_news['articles']

    # citigroup_desc = []
    # citigroup_news = []
    # citigroup_url = []
    # citigroup_time = []

    # for i in range(3):
    #     myarticles = citigroup_articles[i]

    #     citigroup_news.append(myarticles['title'])
    #     citigroup_desc.append(myarticles['description'])
    #     citigroup_url.append(myarticles['url'])
    #     published_time = myarticles['publishedAt']
    #     p = published_time.replace('T', ' ').replace('Z', ' ')
    #     citigroup_time.append(p)

    #citigroup_list = zip(citigroup_news, citigroup_desc, citigroup_url, citigroup_time)


    # Goldman news
    Goldman_news = newsapi.get_everything(q='Goldman',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      language='en',)

    Goldman_articles = Goldman_news['articles']

    Goldman_desc = []
    Goldman_news = []
    Goldman_url = []
    Goldman_time = []

    for i in range(3):
        myarticles = Goldman_articles[i]

        Goldman_news.append(myarticles['title'])
        Goldman_desc.append(myarticles['description'])
        Goldman_url.append(myarticles['url'])
        published_time = myarticles['publishedAt']
        p = published_time.replace('T', ' ').replace('Z', ' ')
        Goldman_time.append(p)

    Goldman_list = zip(Goldman_news, Goldman_desc, Goldman_url, Goldman_time)

    return render(request,'companyProfile.html', locals())


def News(request):
    return render(request,'newstech.html')

def contactUs(request):
    return render(request,'contactUs.html')

def regist(request):
    #if request.method == 'GET':
    #    return render(request, 'signUp.html')
    if request.method == 'POST':
        name = request.POST.get('name', "")
        id = request.POST.get('id', "")
        gender = "Female" if request.POST.get('gender', "") else "Male"
        email = request.POST.get('email', "")
        phone = request.POST.get('phone', "")
        address = request.POST.get('address', "")
        account = request.POST.get('account', "")
        password = request.POST.get('password', "")
        bday = request.POST.get('bday', "")

        # join_member_form = joinMemberForm()


        Member.objects.create(Name=name, ID = id, Gender=gender, Email=email, Phone = phone, Address = address, Account = account, Password = password, BDay=bday)
        return HttpResponseRedirect('/')

@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    if request.method == "POST":
        uf = Form.UserFrom(request.POST)
        if uf.is_valid():
            account = uf.cleaned_data['account']
            password = uf.cleaned_data['password']
            udb = models.Member.objects.filter(Account = account)
            pdb = models.Member.objects.filter(Password = password)
            if udb and pdb:
                request.session['account'] = account
                request.session['is_login'] = True
                return HttpResponseRedirect('/')
            else:
                return render(request,'login.html',{"error": 'The account is wrong!'})
        else:
            uf = Form.UserForm()
            return render(request,'login.html',{"error": 'The account is wrong!'})


def jobselect(request):
    if request.method == 'POST':
        jobName = request.POST.get('jobName')
        request.session['job_name'] = jobName
        return redirect('speech_to_text/equipCheck')

    #if request.method == "GET":
    if 'is_login' in request.session and request.session['is_login']==True:
        user=request.session['account']
        return render(request,'jobselection.html', {'current_user':user})
    else:
        return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

# def equipCheck(request):
#     return render(request, 'equipCheck.html')
