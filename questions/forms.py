from django import forms
from .models import *

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["videofile"]

class SoftwareEngineerForm(forms.ModelForm):
    class Meta:
        model = Software_Engineer
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class DataScientistForm(forms.ModelForm):
    class Meta:
        model = Data_Scientist
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class MISForm(forms.ModelForm):
    class Meta:
        model = MIS
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class HardwareEngineerForm(forms.ModelForm):
    class Meta:
        model = Hardware_Engineer
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class MLEngineerForm(forms.ModelForm):
    class Meta:
        model = ML_Engineer
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

class QuantitativeForm(forms.ModelForm):
    class Meta:
        model = Quantitative
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']

class AuditForm(forms.ModelForm):
    class Meta:
        model = Audit
        fields = ['QuesNum','Difficulties', 'Ques', 'Ans']