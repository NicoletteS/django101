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

class Comment(models.Model):
    text = models.TextField()
    poster = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    date_time = models.DateTimeField(auto_now=True) 
    
    class Meta:
        ordering = ['-date_time']
'''
class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = False)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = False)
	
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

	def save(self,commit = True):
	    user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user '''