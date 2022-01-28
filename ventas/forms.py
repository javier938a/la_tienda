from cProfile import label
from dataclasses import fields
from django import forms
from django.contrib.admin import widgets as wd
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name', 'fecha_nacimiento', 'telefono', 'dui', 'nit')
        labels={
            'username':'Nombre de Usuario',
            'email':'Correo',
            'first_name':'Nombres',
            'last_name':'Apellidos',
            'fecha_nacimiento':'Fecha de Nacimiento',
            'telefono':'telefono',
            'dui':'DUI',
            'nit':'NIT'
        }


