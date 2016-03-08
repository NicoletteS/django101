from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm

# Create your models here.

class Post(models.Model):
    text = models.TextField()
    poster = models.ForeignKey(User)
    date_time = models.DateTimeField(auto_now=True)
    photo = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.text, self.poster, self.date_time

class Comment(models.Model):
    text = models.TextField()
    poster = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    date_time = models.DateTimeField(auto_now=True) 
    
    class Meta:
        ordering = ['-date_time']
    def __str__(self):
        return self.text, self.poster, self.date_time