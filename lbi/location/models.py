from django.db import models

from django import forms

# Create your models here.
class LBI(models.Model):
    Number = models.CharField(max_length=10)
    
    def __str__(self):
        return self.Number
    

class Ean(models.Model):
    lbi = models.ForeignKey(LBI, on_delete=models.CASCADE)
    ean_code = models.CharField(max_length=30)  # Puedes ajustar la longitud según tus necesidades
    created_at = models.DateField(auto_now_add=True)
    is_loaded = models.BooleanField(default=False)

    def __str__(self):
        return f"EAN {self.ean_code} for {self.lbi.Number}"