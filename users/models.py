from django.db import models

# Create your models here.
class Member(models.Model):
    Name = models.CharField(max_length=10)
    ID = models.CharField(max_length=10, primary_key=True)
    Gender = models.CharField(max_length=5)
    Email = models.CharField(max_length=50)
    Phone = models.CharField(max_length=10)
    Address = models.CharField(max_length=100)
    Account = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    BDay = models.DateField(null=False)
    Photo = models.URLField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        result = str(self.Name)
        return result

