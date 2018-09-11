from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

th='data/upload'


class Questions(models.Model):
    questions=models.TextField()
    questiontitle = models.TextField(default="")
    accuracy = models.IntegerField(default=0)
    _submissions = models.IntegerField(default=0)


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    quest1test = models.IntegerField(default=0)
    quest2test = models.IntegerField(default=0)
    quest3test = models.IntegerField(default=0)
    quest4test = models.IntegerField(default=0)
    quest5test = models.IntegerField(default=0)
    quest6test = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    question_id = models.IntegerField(default=0)
    time = models.IntegerField(default=3600)
    date_time = models.DateTimeField(default=datetime.now())
    phone1 = models.CharField(max_length=10)
    phone2 = models.CharField(max_length=10)
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100)
    email1 = models.EmailField()
    email2 = models.EmailField()
    option=models.CharField(max_length=3,default='c')

    def __str__(self):

        return self.user.username


class file(models.Model):
    title = models.CharField(max_length=50,blank=True)
    doc1 = models.FileField(upload_to=th)


class submissions(models.Model):
    sub=models.TextField()
    qid=models.IntegerField(default=0)
    testCaseScore = models.IntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE)