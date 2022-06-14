from django.db import models
from django.forms import CharField

# Create your models here.
class Books(models.Model):
    book_id = models.CharField(max_length=15,default="")
    book_name = models.CharField(max_length=40,default="")
    author_name = models.CharField(max_length=20,default="")