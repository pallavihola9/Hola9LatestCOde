from django.db import models

# Create your models here.
import datetime
class Contact(models.Model):
    Name = models.CharField(max_length=70)
    Email = models.EmailField(max_length=80)
    PhoneNumber = models.IntegerField()
    Message = models.TextField()
    created_at = models.CharField(max_length=150,null=False,blank=False ,default=datetime.datetime.now().strftime('%Y-%m-%d'))