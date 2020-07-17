from django.db import models
from users.models import Member

# Create your models here.
class Software_Engineer(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=500, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ':' + str(self.Ques)
        return result

class Investment_Banking(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=500, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ': ' + str(self.Ques)
        return result

class Answer(models.Model):
    userID = models.ForeignKey(Member,on_delete=models.CASCADE, null=True)
    a1 = models.CharField(max_length=500,blank=True)
    a2 = models.CharField(max_length=500,blank=True)
    a3 = models.CharField(max_length=500,blank=True)
    a4 = models.CharField(max_length=500,blank=True)
    a5 = models.CharField(max_length=500,blank=True)
    a6 = models.CharField(max_length=500,blank=True)
    a6 = models.CharField(max_length=500,blank=True)
    a7 = models.CharField(max_length=500,blank=True)
    a8 = models.CharField(max_length=500,blank=True)
    a9 = models.CharField(max_length=500,blank=True)
    a10 = models.CharField(max_length=500,blank=True)

    def __str__(self):
        result = str(self.id) + ': ' + str(self.a1)
        return result


class Result(models.Model):
    userID = models.ForeignKey(Member,on_delete=models.CASCADE, null=True)
    r1 = models.CharField(max_length=500, blank=True)
    r2 = models.CharField(max_length=500)
    r3 = models.CharField(max_length=500)
    r4 = models.CharField(max_length=500)
    r5 = models.CharField(max_length=500)
    r6 = models.CharField(max_length=500)
    r7 = models.CharField(max_length=500)
    r8 = models.CharField(max_length=500)
    r9 = models.CharField(max_length=500)
    r10 = models.CharField(max_length=500)

    def __str__(self):
        result = str(self.id) + ': ' + str(self.r1)
        return result

class Record(models.Model):
    userID = models.ForeignKey(Member,on_delete=models.CASCADE, null=True)
    rec_a1 = models.CharField(max_length=500, blank=True)
    rec_r1 = models.CharField(max_length=500, blank=True)
    rec_a2 = models.CharField(max_length=500, blank=True)
    rec_r2 = models.CharField(max_length=500, blank=True)
    rec_a3 = models.CharField(max_length=500, blank=True)
    rec_r3 = models.CharField(max_length=500, blank=True)
    rec_a4 = models.CharField(max_length=500, blank=True)
    rec_r4 = models.CharField(max_length=500, blank=True)
    rec_a5 = models.CharField(max_length=500, blank=True)
    rec_r5 = models.CharField(max_length=500, blank=True)
    rec_a6 = models.CharField(max_length=500, blank=True)
    rec_r6 = models.CharField(max_length=500, blank=True)
    rec_a7 = models.CharField(max_length=500, blank=True)
    rec_r7 = models.CharField(max_length=500, blank=True)
    rec_a8 = models.CharField(max_length=500, blank=True)
    rec_r8 = models.CharField(max_length=500, blank=True)
    rec_a9 = models.CharField(max_length=500, blank=True)
    rec_r9 = models.CharField(max_length=500, blank=True)
    rec_a10 = models.CharField(max_length=500, blank=True)
    rec_r10 = models.CharField(max_length=500, blank=True)

    def __str__(self):
        result = str(self.id) + ': ' + str(self.rec_a1)
        return result

class Video(models.Model):
    name= models.CharField(max_length=500)
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.videofile)
