from django.db import models
from django.contrib.auth.models import User
class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    date = models.DateTimeField(auto_now_add=True)
    program = models.CharField(null = True, blank = True, max_length=100)   
    gpa = models.FloatField(null = True, blank = True)
    gre = models.FloatField(null = True, blank = True)
    experience = models.TextField(null = True, blank = True)
    def __str__(self):
        return f"Tokens for {self.user.username}"
    