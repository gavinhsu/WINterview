from django.db import models
from users.models import Member

# Create your models here.
class Software_Engineer(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=800, null=True)
    Keywords = models.TextField(max_length=800, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ':' + str(self.Ques)
        return result

class Data_Scientist(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=800, null=True)
    Keywords = models.TextField(max_length=800, null=True) 

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ': ' + str(self.Ques)
        return result

class DBA(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=800, null=True)
    Keywords = models.TextField(max_length=800, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ': ' + str(self.Ques)
        return result

class ML_Engineer(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=800, null=True)
    Keywords = models.TextField(max_length=800, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ': ' + str(self.Ques)
        return result

class Hardware_Engineer(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=800, null=True)
    Keywords = models.TextField(max_length=800, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ': ' + str(self.Ques)
        return result

class Investment_Banking(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=800, null=True)
    Keywords = models.TextField(max_length=800, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ': ' + str(self.Ques)
        return result

class Sales_Trading(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=800, null=True)
    Keywords = models.TextField(max_length=800, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ': ' + str(self.Ques)
        return result

class Research(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=800, null=True)
    Keywords = models.TextField(max_length=800, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ': ' + str(self.Ques)
        return result

class Quantitative(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=800, null=True)
    Keywords = models.TextField(max_length=800, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ': ' + str(self.Ques)
        return result

class Audit(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=800, null=True)
    Keywords = models.TextField(max_length=800, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ': ' + str(self.Ques)
        return result

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# FOR TESTING PURPOSES ==> DO NOT ADD SHIT INTO THIS MODEL!!!!
# ----------------------------------------------------------------------------------------
class Test_Job_pls_dont_add_shit_into_this_model_thank(models.Model):
    QuesNum = models.IntegerField()
    Difficulties = models.CharField(max_length=100, choices=[('easy','easy'),('medium','medium'),('hard','hard')])
    Ques = models.TextField(max_length=500)
    Ans = models.TextField(max_length=800, null=True)

    def __str__(self):
        result = str(self.QuesNum) + ' ' + str(self.Difficulties) + ': ' + str(self.Ques)
        return result
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------


class Answer(models.Model):
    userID = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    selected_job = models.TextField(blank=True)
    a1 = models.TextField(blank=True)
    v1 = models.TextField(blank=True)
    a2 = models.TextField(blank=True)
    v2 = models.TextField(blank=True)
    a3 = models.TextField(blank=True)
    v3 = models.TextField(blank=True)
    a4 = models.TextField(blank=True)
    v4 = models.TextField(blank=True)
    a5 = models.TextField(blank=True)
    v5 = models.TextField(blank=True)
    a6 = models.TextField(blank=True)
    v6 = models.TextField(blank=True)
    a7 = models.TextField(blank=True)
    v7 = models.TextField(blank=True)
    a8 = models.TextField(blank=True)
    v8 = models.TextField(blank=True)
    a9 = models.TextField(blank=True)
    v9 = models.TextField(blank=True)
    a10 = models.TextField(blank=True)
    v10 = models.TextField(blank=True)

    def __str__(self):
        result = str(self.id) + ': ' + str(self.a1)
        return result


class Result(models.Model):
    userID = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    r1 = models.CharField(max_length=500, blank=True)
    b1 = models.IntegerField(null=True)
    neutral_1 = models.FloatField(null=True, blank=True, default=None)
    happy_1 = models.FloatField(null=True, blank=True, default=None)
    angry_1 = models.FloatField(null=True, blank=True, default=None)
    fear_1 = models.FloatField(null=True, blank=True, default=None)
    surprise_1 = models.FloatField(null=True, blank=True, default=None)
    r2 = models.CharField(max_length=500)
    b2 = models.IntegerField(default=None, null=True)
    neutral_2 = models.FloatField(null=True, blank=True, default=None)
    happy_2 = models.FloatField(null=True, blank=True, default=None)
    angry_2 = models.FloatField(null=True, blank=True, default=None)
    fear_2 = models.FloatField(null=True, blank=True, default=None)
    surprise_2 = models.FloatField(null=True, blank=True, default=None)
    r3 = models.CharField(max_length=500)
    b3 = models.IntegerField(default=None,null=True)
    neutral_3 = models.FloatField(null=True, blank=True, default=None)
    happy_3 = models.FloatField(null=True, blank=True, default=None)
    angry_3 = models.FloatField(null=True, blank=True, default=None)
    fear_3 = models.FloatField(null=True, blank=True, default=None)
    surprise_3 = models.FloatField(null=True, blank=True, default=None)
    r4 = models.CharField(max_length=500)
    b4 = models.IntegerField(default=None,null=True)
    neutral_4 = models.FloatField(null=True, blank=True, default=None)
    neutral_4 = models.FloatField(null=True, blank=True, default=None)
    happy_4 = models.FloatField(null=True, blank=True, default=None)
    angry_4 = models.FloatField(null=True, blank=True, default=None)
    fear_4 = models.FloatField(null=True, blank=True, default=None)
    surprise_4 = models.FloatField(null=True, blank=True, default=None)
    r5 = models.CharField(max_length=500)
    b5 = models.IntegerField(default=None,null=True)
    neutral_5 = models.FloatField(null=True, blank=True, default=None)
    happy_5 = models.FloatField(null=True, blank=True, default=None)
    angry_5 = models.FloatField(null=True, blank=True, default=None)
    fear_5 = models.FloatField(null=True, blank=True, default=None)
    surprise_5 = models.FloatField(null=True, blank=True, default=None)
    r6 = models.CharField(max_length=500)
    b6 = models.IntegerField(default=None,null=True)
    neutral_6 = models.FloatField(null=True, blank=True, default=None)
    happy_6 = models.FloatField(null=True, blank=True, default=None)
    angry_6 = models.FloatField(null=True, blank=True, default=None)
    fear_6 = models.FloatField(null=True, blank=True, default=None)
    surprise_6 = models.FloatField(null=True, blank=True, default=None)
    r7 = models.CharField(max_length=500)
    b7 = models.IntegerField(default=None,null=True)
    neutral_7 = models.FloatField(null=True, blank=True, default=None)
    happy_7 = models.FloatField(null=True, blank=True, default=None)
    angry_7 = models.FloatField(null=True, blank=True, default=None)
    fear_7 = models.FloatField(null=True, blank=True, default=None)
    surprise_7 = models.FloatField(null=True, blank=True, default=None)
    r8 = models.CharField(max_length=500)
    b8 = models.IntegerField(default=None,null=True)
    neutral_8 = models.FloatField(null=True, blank=True, default=None)
    happy_8 = models.FloatField(null=True, blank=True, default=None)
    angry_8 = models.FloatField(null=True, blank=True, default=None)
    fear_8 = models.FloatField(null=True, blank=True, default=None)
    surprise_8 = models.FloatField(null=True, blank=True, default=None)
    r9 = models.CharField(max_length=500)
    b9 = models.IntegerField(default=None,null=True)
    neutral_9 = models.FloatField(null=True, blank=True, default=None)
    happy_9 = models.FloatField(null=True, blank=True, default=None)
    angry_9 = models.FloatField(null=True, blank=True, default=None)
    fear_9 = models.FloatField(null=True, blank=True, default=None)
    surprise_9 = models.FloatField(null=True, blank=True, default=None)
    r10 = models.CharField(max_length=500)
    b10 = models.IntegerField(default=None,null=True)
    neutral_10 = models.FloatField(null=True, blank=True, default=None)
    happy_10 = models.FloatField(null=True, blank=True, default=None)
    angry_10 = models.FloatField(null=True, blank=True, default=None)
    fear_10 = models.FloatField(null=True, blank=True, default=None)
    surprise_10 = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        result = str(self.id) + ': ' + str(self.r1)
        return result

class Record(models.Model):
    userID = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
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
    userID = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    vid1 = models.FileField(upload_to='videos/', null=True, verbose_name="")
    vid2 = models.FileField(upload_to='videos/', null=True, verbose_name="")
    vid3 = models.FileField(upload_to='videos/', null=True, verbose_name="")
    vid4 = models.FileField(upload_to='videos/', null=True, verbose_name="")
    vid5 = models.FileField(upload_to='videos/', null=True, verbose_name="")
    vid6 = models.FileField(upload_to='videos/', null=True, verbose_name="")
    vid7 = models.FileField(upload_to='videos/', null=True, verbose_name="")
    vid8 = models.FileField(upload_to='videos/', null=True, verbose_name="")
    vid9 = models.FileField(upload_to='videos/', null=True, verbose_name="")
    vid10 = models.FileField(upload_to='videos/', null=True, verbose_name="")

    def __str__(self):
        return str(self.id) + ': ' + str(self.vid1)
