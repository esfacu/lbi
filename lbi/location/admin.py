from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LBI, Ean

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'Nombre', 'email', 'is_staff', 'Tienda')  # Ajusta esta lista según tus necesidades
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('Nombre', 'email', 'Tienda')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'Nombre', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'Tienda'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class LBIAdmin(LBI):
    list_display = ('Numero'),
    fieldsets = (
        (None, {
            "fields": (
                'Numero',
            ),
        }),
    )
    
admin.site.register(LBI)
    
    
class EanAdmin(Ean):
    list_display = ('lbi', 'ean_code', 'created_at', 'is_loaded'),
    fieldsets = (
        (None, {
            "fields": (
                'Numero', 'ean_code', 'is_loaded',
            ),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('lbi', 'ean_code', 'created_at', 'is_loaded'),
        }),
    )
admin.site.register(Ean)