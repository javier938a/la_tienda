from django.shortcuts import render
from django.views.generic import TemplateView
from ventas.proces_usuario.crud_usuario import ListarUsuarios, CrearUsuario, EditarUsuario, EliminarUsuario
from ventas.proces_sucursal.crud_sucursal import ListarSucursal, CrearSucursal, EditarSucursal, EliminarSucursal
from ventas.proces_categoria_producto.crud_categoria import ListarCategoriasProducto, CrearCategoriaProducto, EditarCategoriaProducto, EliminarCategoriaProducto
from ventas.proces_producto.crud_producto import ListarProductos, CrearProducto,  EditarProducto, EliminarProducto
from ventas.proces_presentacion.crud_presentacion import ListarPresentacion, CrearPresentacion, EditarPresentacion, EliminarPresentacion
from ventas.proces_inventario.crud_inventario import ListarInventario,  CrearInventario, EditarInventario, EliminarInventario, obtener_productos_autocomplete
from ventas.proces_inventario.crud_inventario import agregar_producto_detalle
# Create your views here.

class Index(TemplateView):
    template_name="ventas/index.html"
