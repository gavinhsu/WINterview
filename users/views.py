from django.shortcuts import render
#from django.views.generic import TemplateViews
from users.models import Member
from django.http import HttpResponseRedirect,HttpResponse

from django.views.decorators.csrf import csrf_exempt
from . import Form,models


def homepage(request):
    return render(request, 'homepage.html')

def signUp(request):
    return render(request, 'signUp.html')
# Create your views here.
'''class JoinMemberView(TemplateView):
    template_name = 'signUp.html'
def get(self, request):
        global join_member_form
        join_member_form = joinMemberForm()
        return render(request, self.template_name, {'form': join_member_form })

def image_view(request):

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = HotelForm()
    return render(request, 'image_form.html', {'form' : form})


    def success(request):
        return HttpResponse('successfully uploaded')


   def post(self, request):
        global join_member_form
        join_member_form = joinMemberForm(request.POST)
        if join_member_form.is_valid():'''
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
                return HttpResponseRedirect('/')
            else:
                #uf = Form.UserFrom({'account':'The account is wrong!'})
                return render(request,'login.html',{"error": 'The account is wrong!'})
        else:
            uf = Form.UserForm()
            return render(request,'login.html',{"error": 'The account is wrong!'})

