from cProfile import label
from dataclasses import field, fields
from pyexpat import model
from django import forms
from django.contrib.admin import widgets as wd
from django.contrib.auth.forms import UserCreationForm
from .models import User, Sucursal, Categoria, Producto, Presentacion

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name','sucursal', 'fecha_nacimiento', 'telefono', 'dui', 'nit')
        labels={
            'username':'Nombre de Usuario',
            'email':'Correo',
            'first_name':'Nombres',
            'last_name':'Apellidos',
            'sucursal':'Sucursal',
            'fecha_nacimiento':'Fecha de Nacimiento',
            'telefono':'telefono',
            'dui':'DUI',
            'nit':'NIT'
        }

class SucursalForm(forms.ModelForm):
    class Meta:
        model=Sucursal
        fields=('logo', 'descripcion', 'direccion', 'telefono')
        labels={
            'logo':'Logo de la Empresa',
            'descripcion':'Descripcion',
            'direccion':'Direccion',
            'telefono':'Telefono'
        }

class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model=Categoria
        fields=('categoria',)
        labels={
            'categoria':'Categoria'
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=("nombre_producto", "descripcion", 'usuario', 'categoria')
        labels={
            'nombre_producto':'Nombre del producto',
            'descripcion':'Descripcion del producto',
            'usuario':'Usuario',
            'categoria':'Categoria del producto'
        }
    
class PresentacionForm(forms.ModelForm):
    class Meta:
        model=Presentacion
        fields=('presentacion',)
        labels={
            'presentacion':'Presentacion'
        }
