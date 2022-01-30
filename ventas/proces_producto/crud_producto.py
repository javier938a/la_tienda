from pyexpat import model

from django.urls import reverse_lazy
from ventas.models import Producto
from ventas.forms import ProductoForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

class CrearProducto(CreateView):
    template_name="proces_producto/crear_producto.html"
    model=Producto
    form_class=ProductoForm
    context_object_name="form"
    success_url=reverse_lazy("store:list_prod")

class ListarProductos(ListView):
    template_name="proces_producto/listar_producto.html"
    model=Producto
    context_object_name="producto"
    