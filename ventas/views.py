from django.shortcuts import render
from django.views.generic import TemplateView
from ventas.proces_usuario.crud_usuario import ListarUsuarios, CrearUsuario, EditarUsuario, EliminarUsuario

# Create your views here.

class Index(TemplateView):
    template_name="ventas/index.html"
