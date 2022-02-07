from django.contrib import admin
from .models import User, Sucursal, Categoria, Presentacion, Producto, ProductoStockSucursal, ProductoStockGlobal
from .models import FacturaVentas, Ventas, InventarioProductos
# Register your models here.

admin.site.register(User)
admin.site.register(Sucursal)
admin.site.register(Categoria)
admin.site.register(Presentacion)
admin.site.register(Producto)
admin.site.register(ProductoStockSucursal)
admin.site.register(FacturaVentas)
admin.site.register(Ventas)
admin.site.register(ProductoStockGlobal)
admin.site.register(InventarioProductos)