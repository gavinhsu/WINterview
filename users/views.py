from django.shortcuts import render
from django.views.generic import TemplateView

def homepage(request):
    return render(request, 'homepage.html')

def signUp(request):
    return render(request, 'signUp.html')
# Create your views here.

class JoinMemberView(TemplateView):
    template_name = 'signUp.html'
    def get(self, request):
        global join_member_form
        join_member_form = joinMemberForm()
        return render(request, self.template_name, {'form': join_member_form })

    ''' def image_view(request):

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = HotelForm()
    return render(request, 'image_form.html', {'form' : form})


    def success(request):
        return HttpResponse('successfully uploaded')'''


    def post(self, request):
        global join_member_form
        join_member_form = joinMemberForm(request.POST)
        if join_member_form.is_valid():
            name = request.POST.get('name', "")
            id = request.POST.get('id', "")
            gender = "Female" if request.POST.get('gender', "") else "Male"
            email = request.POST.get('email', "")
            phone = request.POST.get('phone', "")
            address = request.POST.get('address', "")
            account = request.POST.get('account', "")
            password = request.POST.get('password', "")
            bday = request.POST.get('bday', "")
            join_member_form = joinMemberForm()


            Member.objects.create(mName=name, ID = id,Gender=gender, Email=email, Phone = phone, Address = address, Account = account,Password = password, BDay=bday)
            
            return render(request, self.template_name, {
                    'form': join_member_form,
                    'res': "恭喜 " + new_member.mName + " 已成為會員"
                    })
        else:
            return render(request, self.template_name, {
                    'form': join_member_form,
                    'res': "表單驗證失敗，無法加入會員"
                    })
