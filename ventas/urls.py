from unicodedata import name
from django.urls import path


from .views import Index
from .views import ListarUsuarios, CrearUsuario, EditarUsuario, EliminarUsuario
from .views import ListarProveedor, CrearProveedor, EditarProveedor, EliminarProveedor
from .views import ListarSucursal, CrearSucursal, EditarSucursal, EliminarSucursal
from .views import ListarCategoriasProducto, CrearCategoriaProducto, EditarCategoriaProducto, EliminarCategoriaProducto
from .views import ListarProductos, CrearProducto, EditarProducto, EliminarProducto
from .views import ListarPresentacion, CrearPresentacion, EditarPresentacion, EliminarPresentacion
from .views import ListarInventario, ViewCrearInventario, ViewEditarInventario, EliminarInventario, obtener_productos_autocomplete, agregar_producto_detalle
from .views import guardar_datos_inventario, actualizar_datos_inventario, update_producto_detalle, DetalleInventario
from .views import ListarVentas, ViewCrearVenta, ViewDetalleVenta, verificar_stock_producto, obtener_productos_inventario_autocomplete, agregar_producto_detalle_venta, efectuar_venta


app_name="store"
urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('usuarios/', ListarUsuarios.as_view(), name="user"),
    path('usuarios/crear_usuarios', CrearUsuario.as_view(), name="crear_user"),
    path('usuarios/editar_usuario/<int:pk>', EditarUsuario.as_view(), name="editar_user"),
    path('usuarios/eliminar_usuario/<int:pk>', EliminarUsuario.as_view(), name="del_user"),
    path('proveedores/', ListarProveedor.as_view(), name="list_prove"),
    path('proveedores/crear_proveedor', CrearProveedor.as_view(), name="crear_prove"),
    path('proveedores/editar_proveedor/<int:pk>', EditarProveedor.as_view(), name="edit_prove"),
    path('proveedores/eliminar_proveedor/<int:pk>', EliminarProveedor.as_view(), name="del_prove"),
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
    path('inventario/crear_inventario', ViewCrearInventario.as_view(), name="crear_inv"),
    path('inventario/editar_inventario/<int:pk>', ViewEditarInventario.as_view(), name="edit_inv"),
    path('inventario/detalle_inventario/<int:pk>', DetalleInventario.as_view(), name="det_inv"),
    path('inventario/eliminar_inventario/<int:pk>', EliminarInventario.as_view(), name="del_inv"),
    path('inventario/auto_prod_list', obtener_productos_autocomplete, name='auto_prod_list'),
    path('inventario/agregar_producto', agregar_producto_detalle, name="add_prod_detalle"),
    path('inventario/guardar_detalles_inventario', guardar_datos_inventario, name='guardar_dato_inventario'),
    path('inventario/actualizar_inventario', actualizar_datos_inventario, name='add_update_detalle_inv'),
    path('inventario/agregar_prod_update', update_producto_detalle, name="add_update_inv"),
    path('ventas/', ListarVentas.as_view(), name="list_venta"),
    path('ventas/crear_venta', ViewCrearVenta.as_view(), name="crear_venta"),
    path('ventas/detalle_de_venta/<int:pk>', ViewDetalleVenta.as_view(), name='detalle_venta'),
    path('ventas/productos_autocomplete_inv', obtener_productos_inventario_autocomplete, name='prod_inv_autocomplete'),
    path('ventas/agregar_productos_detalle_venta', agregar_producto_detalle_venta, name='add_prod_venta'),
    path('ventas/efectuar_venta', efectuar_venta, name='efectuar_venta'),
    path('ventas/verificar_stock_producto', verificar_stock_producto, name="verificar_stock")
]