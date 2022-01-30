from django.contrib import admin
from .models import User, Sucursal, Categoria, Presentacion, Producto, StockSucursal, StockGloval
# Register your models here.

admin.site.register(User)
admin.site.register(Sucursal)
admin.site.register(Categoria)
admin.site.register(Presentacion)
admin.site.register(Producto)
admin.site.register(StockSucursal)
admin.site.register(StockGloval)