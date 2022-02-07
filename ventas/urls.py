from unicodedata import name
from django.urls import path
from .views import Index
from .views import ListarUsuarios, CrearUsuario, EditarUsuario, EliminarUsuario
from .views import ListarSucursal, CrearSucursal, EditarSucursal, EliminarSucursal
from .views import ListarCategoriasProducto, CrearCategoriaProducto, EditarCategoriaProducto, EliminarCategoriaProducto
from .views import ListarProductos, CrearProducto, EditarProducto, EliminarProducto
from .views import ListarPresentacion, CrearPresentacion, EditarPresentacion, EliminarPresentacion
from .views import ListarInventario, CrearInventario, EditarInventario, EliminarInventario, obtener_productos_autocomplete, agregar_producto_detalle
from .views import guardar_datos_inventario


app_name="store"
urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('usuarios/', ListarUsuarios.as_view(), name="user"),
    path('usuarios/crear_usuarios', CrearUsuario.as_view(), name="crear_user"),
    path('usuarios/editar_usuario/<int:pk>', EditarUsuario.as_view(), name="editar_user"),
    path('usuarios/eliminar_usuario/<int:pk>', EliminarUsuario.as_view(), name="del_user"),
    path('sucursales/', ListarSucursal.as_view(), name="list_sucursal"),
    path('sucursales/crear_sucursal', CrearSucursal.as_view(), name="crear_sucursal"),
    path('sucursales/editar_sucursal/<int:pk>', EditarSucursal.as_view(), name="edit_sucursal"),
    path('sucursales/eliminar_sucursal/<int:pk>', EliminarSucursal.as_view(), name="del_sucursal"),
    path('categorias_producto/', ListarCategoriasProducto.as_view(), name="list_cate"),
    path('categorias_producto/crear_categoria_producto', CrearCategoriaProducto.as_view(), name="crear_cate"),
    path('categorias_producto/editar_categoria_producto/<int:pk>', EditarCategoriaProducto.as_view(), name="edit_cate"),
    path('categorias_producto/eliminar_categoria_producto/<int:pk>', EliminarCategoriaProducto.as_view(), name="del_cate"),
    path('productos/', ListarProductos.as_view(), name="list_prod"),
    path('productos/crear_producto', CrearProducto.as_view(), name="crear_prod"),
    path('productos/editar_producto/<int:pk>', EditarProducto.as_view(), name="editar_prod"),
    path('productos/eliminar_producto/<int:pk>', EliminarProducto.as_view(), name="del_prod"),
    path('presentaciones/', ListarPresentacion.as_view(), name="list_pre"),
    path('presentaciones/crear_presentacion', CrearPresentacion.as_view(), name="crear_pre"),
    path('presentaciones/editar_presentacion/<int:pk>', EditarPresentacion.as_view(), name="edit_pre"),
    path('presentacion/eliminar_presentacion/<int:pk>', EliminarPresentacion.as_view(), name="del_pre"),
    path('inventario/', ListarInventario.as_view(), name="list_inv"),
    path('inventario/crear_inventario', CrearInventario.as_view(), name="crear_inv"),
    path('inventario/editar_inventario/<int:pk>', EditarInventario.as_view(), name="edit_inv"),
    path('inventario/eliminar_inventario/<int:pk>', EliminarInventario.as_view(), name="del_inv"),
    path('inventario/auto_prod_list', obtener_productos_autocomplete, name='auto_prod_list'),
    path('inventario/agregar_producto', agregar_producto_detalle, name="add_prod_detalle"),
    path('inventario/guardar_detalles_inventario', guardar_datos_inventario, name='guardar_dato_inventario')
]