from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DeleteView, UpdateView, TemplateView, CreateView
from django.urls import reverse_lazy
from .models import LBI
from .forms import LBIForm

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