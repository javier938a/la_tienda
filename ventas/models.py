from ast import Mod
from itertools import product
from pyexpat import model
from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.base import Model

# Create your models here.

class UserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

class Sucursal(models.Model):
    logo=models.ImageField(verbose_name="logo", upload_to="logo_sucursal", null=True, blank=True)
    descripcion=models.CharField(max_length=50, help_text="Ingrese una descripcion de la sucursal")
    direccion=models.TextField(help_text="Ingrese la direccion de la tienda")
    telefono=models.CharField(max_length=50, help_text="Ingrese el telefono de la ubicacion")

    def __str__(self) -> str:
        return self.descripcion

class User(AbstractUser):
    objects=UserManager()
    sucursal=models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    fecha_nacimiento=models.DateField(null=True, blank=True, help_text="Ingrese la fecha de nacimiento")
    telefono=models.CharField(max_length=11, help_text="Ingrese su numero de telefono", null=True, blank=True)
    dui=models.CharField(max_length=10, help_text="Ingrese el numero de dui", null=True, blank=True)
    nit=models.CharField(max_length=19, help_text="Ingrese el numero de dui", null=True, blank=True)

    class Meta:
        db_table="auth_user"
    
    def natural_key(self):
        return (self.username)

class Categoria(models.Model):
    categoria=models.CharField(max_length=50, help_text="Ingrese la categoria del producto", null=True)

    def __str__(self) -> str:
        return "%s"%str(self.categoria) 

class Producto(models.Model):
    nombre_producto=models.CharField(max_length=100, help_text="Ingrese el nombre del producto")
    descripcion=models.CharField(max_length=100, help_text="Ingrese la descripcion del producto")
    usuario=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categoria=models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return "%s"%self.nombre_producto

class Presentacion(models.Model):
    presentacion=models.CharField(max_length=50, help_text="Ingrese la presentacion")

    def __str__(self) -> str:
        return "%s"%self.presentacion


class StockSucursal(models.Model):
    sucursal=models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    producto=models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    presentacion=models.ForeignKey(Presentacion, on_delete=models.SET_NULL, null=True)
    cantidad=models.IntegerField(help_text="Ingrese la cantidad de producto")
    precio=models.DecimalField(help_text="Ingrese la cantidad", decimal_places=2, max_digits=10)
    total=models.DecimalField(help_text="", decimal_places=2, max_digits=10)

    def __str__(self) -> str:
        return "%s -> %s"%(self.sucursal, self.producto)

class StockGloval(models.Model):
    producto=models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    presentacion=models.ForeignKey(Presentacion, on_delete=models.SET_NULL, null=True)
    cantidad=models.IntegerField(help_text="Ingrese la cantidad del producto global")
    precio=models.DecimalField(help_text="Ingrese el precio del producto", decimal_places=2, max_digits=10)
    total=models.DecimalField(help_text="", decimal_places=2, max_digits=10)

    def __str__(self) -> str:
        return "%s -> %s"%(self.producto, str(self.cantidad))
