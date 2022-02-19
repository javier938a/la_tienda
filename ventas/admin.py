from django.contrib import admin
from .models import User, Sucursal, Categoria, Presentacion, Producto, ProductoStockSucursal, ProductoStockGlobal
from .models import Venta, DetalleVenta, InventarioProductos, CargaProductos, DetalleCargaProductos
# Register your models here.

admin.site.register(User)
admin.site.register(Sucursal)
admin.site.register(Categoria)
admin.site.register(Presentacion)
admin.site.register(Producto)
admin.site.register(ProductoStockSucursal)
admin.site.register(DetalleVenta)
admin.site.register(Venta)
admin.site.register(ProductoStockGlobal)
admin.site.register(InventarioProductos)
admin.site.register(CargaProductos)
admin.site.register(DetalleCargaProductos)