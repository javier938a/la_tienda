from itertools import product
from django.views.generic import ListView, TemplateView
from ventas.models import ProductoStockSucursal
from ventas.models import DescargaProductos, DetalleDescargaProducto
from django.db.models import Q
from django.http import JsonResponse

class ListarDescargasProductos(ListView):
    template_name="proces_descarga_productos/listar_descargas_productos.html"
    model=DescargaProductos
    context_object_name="descarga_prod"

class ViewCrearDescargaProducto(TemplateView):
    template_name="proces_descarga_productos/crear_descarga_productos.html"


def listar_productos_a_descargar_por_sucursal_autocomplete(request):
    clave = request.POST.get('term')
    print(clave)
    sucursal=request.user.sucursal
    productos=None
    datos=[]
    if(clave.strip()!=''):
        lista_productos=ProductoStockSucursal.objects.filter(sucursal=sucursal).filter(Q(producto__nombre_producto__icontains=clave)|Q(producto__descripcion__icontains=clave)|Q(producto__codigo_producto=clave))
        for prod in lista_productos:
            fila=str(prod.id)+'|'+str(prod.producto.nombre_producto)+'|'+str(prod.producto.descripcion)+'|'+str(prod.cantidad)
            datos.append(fila)
    else:
        lista_productos=ProductoStockSucursal.objects.filter(sucursal=sucursal)
        for prod in lista_productos:
            fila=str(prod.id)+'|'+str(prod.producto.nombre_producto)+'|'+str(prod.producto.descripcion)+'|'+str(prod.cantidad)
            datos.append(fila)
    
    return JsonResponse(datos, safe=False)


def agregar_producto_a_descargar_a_detalle(request):
    id_prod_stock=request.POST.get('id_prod_stock')
    
    producto_stock_ubi=ProductoStockSucursal.objects.get(id=id_prod_stock)
    fila_producto='<tr>'
    fila_producto+='<td><input class="form-control idprod" type="text" value="'+str(producto_stock_ubi.id)+'" disabled></td>'
    fila_producto+='<td><input class="form-control" type="text" value="'+str(producto_stock_ubi.producto.nombre_producto)+'" disabled></td>'
    fila_producto+='<td><input class="form-control" type="text" value="'+str(producto_stock_ubi.producto.descripcion)+'" disabled></td>'
    fila_producto+='<td><input class="form-control" type="text" value="'+str(producto_stock_ubi.presentacion)+'" disabled></td>'
    fila_producto+='<td><input class="form-control" type="text" value="'+str(producto_stock_ubi.cantidad)+'" disabled></td>'
    fila_producto+='<td><input class="form-control cant" type="text" value=""></td>'
    fila_producto+='<td><input class="form-control cost" type="text" value="'+str(producto_stock_ubi.costo)+'" disabled></td>'
    fila_producto+='<td><input class="form-control tot" type="text" value="" disabled></td>'
    fila_producto+='<td><input class="btn btn-danger form-control delfila" type="button" value="Eliminar"></td>'
    fila_producto+='</tr>'

    datos={
        'fila_producto':fila_producto,
    }
    return JsonResponse(datos, safe=False)

