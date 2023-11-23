from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DeleteView, UpdateView, TemplateView, CreateView
from django.urls import reverse_lazy
from .models import LBI, Ean
from .forms import LBIForm , LBISelectionForm, EanCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.http import HttpResponse
import csv
from django.db.models import F

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
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
    
    
class LBIListView(ListView):
    model = LBI
    template_name = 'ubication/ubication.html'
    context_object_name = 'ubication'
    

class EanListView(ListView):
    model = Ean
    template_name = 'eans/locations.html'
    context_object_name = 'eans'
 
''' 
class LBIUpdateView(PermissionRequiredMixin,UpdateView):
    model = LBI
    template_name = 'ubication/update_ubication.html'
    fields = ['Number']
    success_url = reverse_lazy('ubication')
    permission_required = 'location.update_lbi'
    permission_denied_message = 'No estas autorizado'
    
    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return render(self.request, 'errores/403.html', status=403)
    
    from django.contrib.auth.mixins import LoginRequiredMixin  # Importa solo LoginRequiredMixin
'''
class LBIUpdateView(UpdateView):  # Usa solo LoginRequiredMixin
    model = LBI
    template_name = 'ubication/update_ubication.html'
    fields = ['Number']
    success_url = reverse_lazy('ubication')
    

def select_lbi(request):
    if request.method == 'POST':
        form = LBISelectionForm(request.POST)
        if form.is_valid():
            selected_lbi_id = form.cleaned_data['selected_lbi']
            request.session['selected_lbi_id'] = selected_lbi_id
            return redirect('create_ean')
    else:
        form = LBISelectionForm()

    return render(request, 'eans/select_lbi.html', {'form': form})


def create_ean(request):
    selected_lbi_id = request.session.get('selected_lbi_id')
    selected_lbi = LBI.objects.get(pk=selected_lbi_id)

    if request.method == 'POST':
        form = EanCreationForm(request.POST)
        if form.is_valid():
            ean_code = form.cleaned_data['ean_code']
            Ean.objects.create(lbi=selected_lbi, ean_code=ean_code)
            messages.success(request, 'EAN agregado exitosamente.')
            return redirect('create_ean')
    else:
        form = EanCreationForm()

    return render(request, 'eans/create_ean.html', {'form': form, 'selected_lbi': selected_lbi})

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
        ean_data = Ean.objects.values('ean_code', 'lbi__Number')

        # Crear la respuesta del archivo CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ean_data.csv"'

        # Crear el escritor CSV y escribir los encabezados
        writer = csv.writer(response)
        writer.writerow(['EAN Code', 'LBI Number'])

        # Escribir los datos en el archivo CSV
        for row in ean_data:
            writer.writerow([row['ean_code'], row['lbi__Number']])

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
    query = request.GET.get('q')
    if query:
        eans = Ean.objects.filter(ean_code__icontains=query)
        if not eans:
            messages.info(request, 'No se encontró ningún Ean.')
    else:
        eans = Ean.objects.all()
    return render(request, 'eans/locations.html', {'eans': eans, 'query': query})