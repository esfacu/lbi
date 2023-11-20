from django.db import models

from django import forms

# Create your models here.
class LBI(models.Model):
    Number = models.CharField(max_length=10)
    
    def __str__(self):
        return self.Number