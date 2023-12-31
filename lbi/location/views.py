from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
#Decoradores 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
#Vistas
from django.views.generic import ListView, DeleteView, UpdateView, TemplateView, CreateView
from django.urls import reverse_lazy
from .models import LBI, Ean
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.http import HttpResponse
import csv
from django.db.models import F

# Create your views here.

class Error403View(TemplateView):
    template_name = 'errores/403.html'

@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'
  
@method_decorator(login_required, name='dispatch')
class LBICreateView(CreateView):
    model = LBI
    form_class = LBIForm
    template_name = 'ubication/form_lbi.html'
    success_url = reverse_lazy('lbi_create')

    def form_valid(self, form):
        messages.success(self.request, 'Ubicación agregada exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lbi_create')
    
@method_decorator(login_required, name='dispatch')
class LBIListView(ListView):
    model = LBI
    template_name = 'ubication/ubication.html'
    context_object_name = 'ubication'
    
@method_decorator(login_required, name='dispatch')
class EanListView(ListView):
    model = Ean
    template_name = 'eans/locations.html'
    context_object_name = 'eans'
 
@method_decorator(login_required, name='dispatch')
class LBIUpdateView(UpdateView):  # Usa solo LoginRequiredMixin
    model = LBI
    template_name = 'ubication/update_ubication.html'
    fields = ['Number']
    success_url = reverse_lazy('ubication')
    
@login_required
def select_lbi(request):
    if request.method == 'POST':
        form = LBISelectionForm(request.POST)
        if form.is_valid():
            selected_lbi = form.cleaned_data['selected_lbi']

            try:
                selected_lbi_instance = LBI.objects.get(Number=selected_lbi)
            except LBI.DoesNotExist:
                messages.error(request, 'El LBI seleccionado no existe. Por favor, elige uno válido o Agregalo en Add Rack.')
                return render(request, 'eans/select_lbi.html', {'form': form})

            request.session['selected_lbi'] = selected_lbi
            return redirect('create_ean')
    else:
        form = LBISelectionForm()

    return render(request, 'eans/select_lbi.html', {'form': form})


@login_required
def create_ean(request):
    selected_lbi_id = request.session.get('selected_lbi') 
    selected_lbi_instance = LBI.objects.get(Number=selected_lbi_id)
    
    if request.method == 'POST':
        form = EanCreationForm(request.POST)
        if form.is_valid():
            ean_code = form.cleaned_data['ean_code']
            # Obtener el usuario actual
            colaborador_actual = request.user
            # Aquí asignamos la instancia de LBI al campo lbi
            ean = Ean(lbi=selected_lbi_instance, ean_code=ean_code, colaborador=colaborador_actual)
            
            ean.save()
            messages.success(request, 'EAN agregado exitosamente.')
            return redirect('create_ean')
    else:
        form = EanCreationForm()

    return render(request, 'eans/create_ean.html', {'form': form, 'selected_lbi': selected_lbi_instance})

@method_decorator(login_required, name='dispatch')
class LocationUpdateView(UpdateView):  # Usa solo LoginRequiredMixin
    model = Ean
    template_name = 'eans/update_location.html'
    fields = ['lbi', 'ean_code', 'is_loaded']
    success_url = reverse_lazy('location')
    

def search(request):
    query = request.GET.get('q')
    resultados = LBI.objects.filter(Number__icontains=query) if query else None

    return render(request, 'search.html', {'query': query, 'resultados': resultados})


class ExportCSVView(View):
    def get(self, request, *args, **kwargs):
        # Obtener los datos que quieres incluir en el CSV
        ean_data = Ean.objects.values('ean_code', 'lbi__Number', 'colaborador__Tienda','is_loaded')

        # Crear la respuesta del archivo CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ean_data.csv"'

        # Crear el escritor CSV y escribir los encabezados
        writer = csv.writer(response)
        writer.writerow(['EAN Code', 'LBI Number', 'Tienda', 'is_loaded?'])

        # Escribir los datos en el archivo CSV
        for row in ean_data:
            writer.writerow([row['ean_code'], row['lbi__Number'], row['colaborador__Tienda'], row['is_loaded']])

        return response

    
class ConfirmarActualizacionView(View):
    def get(self, request, *args, **kwargs):
        # Actualiza el campo is_loaded de False a True
        Ean.objects.filter(is_loaded=False).update(is_loaded=True)
        return redirect('location')  
    
class EliminarBaseView(View):
    def get(self, request, *args, **kwargs):
        #Elimina todos los registros del modelo Ean
        Ean.objects.all().delete()
        return redirect('location') #Re dirige a location
    

class EliminarRackView(View):
    def get(self, request, pk):
        # Obtén la instancia del modelo que deseas eliminar
        rack = get_object_or_404(LBI, Number=pk)
        
        # Elimina la instancia
        rack.delete()

        # Redirige a la página 'ubication' después de la eliminación
        return redirect('ubication')
    

class EliminarEanView(View):
    def get(self, request, pk):
        # Obtén la instancia del modelo que deseas eliminar
        ean = get_object_or_404(Ean, id=pk)
        
        # Elimina la instancia
        ean.delete()

        # Redirige a la página 'ubication' después de la eliminación
        return redirect('location')
    
    
def searchEan(request):
    # Obtener el valor de búsqueda del formulario
    query = request.GET.get('q')
    # Obtener el valor de is_loaded del formulario
    is_loaded_filter = request.GET.get('is_loaded')

    # Inicializar queryset con todos los EANs
    eans = Ean.objects.all()

    # Si hay un término de búsqueda, filtrar por ese término
    if query:
        eans = eans.filter(ean_code__icontains=query)
        if not eans:
            messages.info(request, 'No se encontró ningún EAN.')

    # Si hay un filtro is_loaded, aplicar el filtro
    if is_loaded_filter is not None:
        is_loaded_value = True if is_loaded_filter.lower() == 'true' else False
        eans = eans.filter(is_loaded=is_loaded_value)

    # Renderizar la plantilla con los resultados
    return render(request, 'eans/locations.html', {'eans': eans, 'query': query})


def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Cédula incorrecta o usuario no encontrado.')
        else:
            messages.error(request, 'Formulario inválido. Verifica los datos ingresados.')
            print(form.errors)
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso!')# Redirige a donde quieras después del registro
            return redirect('index')
        else:
            # Pasa los errores al contexto
            messages.error(request, 'La contraseña debe contener al menos 8 caracteres')
            messages.error(request, 'La contraseña  no puede ser totalmente numérica, debe tener al menos 2 letras')
            return render(request, 'login/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'login/register.html', {'form': form})  # Reemplaza 'nombre_de_tu_template.html' con la ruta correcta a tu template
