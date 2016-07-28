from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Label(models.Model):
    user = models.ForeignKey(User,related_name='labels')
    name = models.CharField(max_length=40)

class Note(models.Model):
    user = models.ForeignKey(User,related_name='notes')
    name = models.CharField(max_length=40)
    body = models.CharField(max_length=1000)
    labels = models.ManyToManyField(Label)
