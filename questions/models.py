from django.db import models
from users.models import Member

# Create your models here.
class Question(models.Model):
    QuesNum = models.CharField(max_length=10000)
    Field = models.CharField(max_length=100)
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=500, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Field) + ':' + str(self.Ques)
        return result

class Answer(models.Model):
    userID = models.ForeignKey(Member,on_delete=models.CASCADE, null=True)
    a1 = models.CharField(max_length=500,blank=True)
    a2 = models.CharField(max_length=500)
    a3 = models.CharField(max_length=500)
    a4 = models.CharField(max_length=500)
    a5 = models.CharField(max_length=500)
    a6 = models.CharField(max_length=500)
    a6 = models.CharField(max_length=500)
    a7 = models.CharField(max_length=500)
    a8 = models.CharField(max_length=500)
    a9 = models.CharField(max_length=500)
    a10 = models.CharField(max_length=500)

    def __str__(self):
        result = str(self.id) + ':' + str(self.a1)
        return result

