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
    
class University(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    ranking = models.IntegerField()
    acceptance_rate = models.FloatField()
    avg_gre = models.FloatField()
    avg_gpa = models.FloatField()    
    def __str__(self):
        return f'{self.name} - {self.location} -  {self.ranking} - {self.acceptance_rate} -  {self.avg_gre} - {self.avg_gpa}'