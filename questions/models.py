from django.db import models

# Create your models here.
class Question(models.Model):
    QuesNum = models.CharField(max_length=10000)
    Field = models.CharField(max_length=100)
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=500)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Field) +str(self.Ques)
        return result


