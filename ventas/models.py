from ast import Mod
from pyexpat import model
from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.base import Model

# Create your models here.

class UserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractUser):
    objects=UserManager()
    fecha_nacimiento=models.DateField(null=True, blank=True, help_text="Ingrese la fecha de nacimiento")
    telefono=models.CharField(max_length=11, help_text="Ingrese su numero de telefono", null=True, blank=True)
    dui=models.CharField(max_length=10, help_text="Ingrese el numero de dui", null=True, blank=True)
    nit=models.CharField(max_length=19, help_text="Ingrese el numero de dui", null=True, blank=True)

    class Meta:
        db_table="auth_user"
    
    def natural_key(self):
        return (self.username)
