from django import forms
from .models import *
class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ["name", "videofile"]

class SoftwareEngineerForm(forms.ModelForm):
    class Meta:
        model = Software_Engineer
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class DataScientistForm(forms.ModelForm):
    class Meta:
        model = Data_Scientist
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class DatabaseAdministratorForm(forms.ModelForm):
    class Meta:
        model = Database_Administrator
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class NetworkEngineerForm(forms.ModelForm):
    class Meta:
        model = Network_Engineer
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class InvestmentBankingForm(forms.ModelForm):
    class Meta:
        model = Investment_Banking
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class SalesTradingForm(forms.ModelForm):
    class Meta:
        model = Sales_Trading
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class QuantitativeTradingForm(forms.ModelForm):
    class Meta:
        model = Quantitative_Trading
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class Venture_CapitalForm(forms.ModelForm):
    class Meta:
        model = Venture_Capital
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']