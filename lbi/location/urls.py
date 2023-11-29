"""
URL configuration for lbi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('ubication/', LBIListView.as_view(), name='ubication'),
    path('', IndexView.as_view(), name='index'),
    path('lbi/create/', LBICreateView.as_view(), name='lbi_create'),
    path('ubication/<int:pk>/update_ubication/', LBIUpdateView.as_view(), name='update_ubication'),
    path('select_lbi/', select_lbi, name='select_lbi'),
    path('eliminar-rack/<str:pk>', EliminarRackView.as_view(), name='eliminar_rack'),
    #ean
    path('location/', EanListView.as_view(), name='location'),
    path('create_ean/', create_ean, name='create_ean'),
    path('location/<int:pk>/update_location/', LocationUpdateView.as_view(), name='update_location'),
    path('eliminar-ean/<str:pk>', EliminarEanView.as_view(), name='eliminar_ean'),
    #Search bar
    path('search/', search , name='search'),
    path('searchEan', searchEan, name='searchEan'),
    #Descarga CSV
    path('export-csv/', ExportCSVView.as_view(), name='export_csv'),
    path('confirmar-actualizacion/', ConfirmarActualizacionView.as_view(), name='confirmar_actualizacion'),
    path('eliminar-base/', EliminarBaseView.as_view(), name='eliminar_base'),
    #Login
    path('login/', custom_login, name='custom_login'),
    #logout
    path('login/', LogoutView.as_view(), name='logout'),
    #register
    path('register/', register, name='register'),
]
