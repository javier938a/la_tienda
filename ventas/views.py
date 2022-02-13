from django.shortcuts import render
from django.views.generic import TemplateView
from ventas.proces_usuario.crud_usuario import ListarUsuarios, CrearUsuario, EditarUsuario, EliminarUsuario
from ventas.proces_proveedor.crud_proveedor import ListarProveedor, CrearProveedor, EditarProveedor, EliminarProveedor
from ventas.proces_sucursal.crud_sucursal import ListarSucursal, CrearSucursal, EditarSucursal, EliminarSucursal
from ventas.proces_categoria_producto.crud_categoria import ListarCategoriasProducto, CrearCategoriaProducto, EditarCategoriaProducto, EliminarCategoriaProducto
from ventas.proces_producto.crud_producto import ListarProductos, CrearProducto,  EditarProducto, EliminarProducto
from ventas.proces_presentacion.crud_presentacion import ListarPresentacion, CrearPresentacion, EditarPresentacion, EliminarPresentacion
from ventas.proces_inventario.crud_inventario import ListarInventario,  ViewCrearInventario, ViewEditarInventario, EliminarInventario, obtener_productos_autocomplete
from ventas.proces_inventario.crud_inventario import DetalleInventario, agregar_producto_detalle, guardar_datos_inventario, actualizar_datos_inventario, update_producto_detalle
from ventas.proces_venta.crud_venta import ListarVentas, ViewCrearVenta, ViewDetalleVenta, obtener_productos_inventario_autocomplete, agregar_producto_detalle_venta, efectuar_venta

# Create your views here.

class Index(TemplateView):
    template_name="ventas/index.html"
