from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django import forms

# Create your models here.
class LBI(models.Model):
    Number = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.Number
    
class CustomUser(AbstractUser):
    username = models.CharField(max_length=8, unique=True) 
    Nombre = models.CharField(max_length=30)
        
    TIENDA_CHOICES = [
        ('Dmart5','"UY_5_Ciudad de la Costa"'),
        ('Dmart12','"UY_12_Aguada"'),
        ('Dmart7','"UY_7_Sayago"'),
        ('Dmart4','"UY_4_Centro"'),
        ('Dmart9','"UY_9_La Blanqueada"'),
        ('Dmart10','"UY_10_Carrasco Norte"'),
        ('Dmart11','"UY_11_Brazo Oriental"'),
        ('Dmart6','"UY_6_Maldonado"'),
        ('Dmart8','"UY_8_Malvin Norte"'),
        ('Dmart13','"UY_13_Tres Cruces"'),  
    ]
        
    Tienda = models.CharField(max_length=10, choices=TIENDA_CHOICES)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Nombre diferente para el campo inverso
        related_query_name='customuser',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Nombre diferente para el campo inverso
        related_query_name='customuser',
        blank=True,
        help_text='Specific permissions for this user.',
    )
    
    def __str__(self):
        return self.username

    
class Ean(models.Model):
    lbi = models.ForeignKey(LBI, on_delete=models.CASCADE)
    colaborador = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ean_code = models.CharField(max_length=30)  # Puedes ajustar la longitud según tus necesidades
    created_at = models.DateField(auto_now_add=True)
    is_loaded = models.BooleanField(default=False)

    def __str__(self):
        return f"EAN {self.ean_code} for {self.lbi.Number}"



            