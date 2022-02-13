from math import prod
from multiprocessing import context
from pyexpat import model
from django.views.generic import ListView, TemplateView, DetailView
from ventas.models import Venta, DetalleVenta, Sucursal, ProductoStockSucursal, User
from django.db.models import Q
from django.http import JsonResponse
from django.core.serializers import serialize
import json

class ViewCrearVenta(TemplateView):
    template_name="proces_venta/crear_venta.html"
    def get_context_data(self, **kwargs):
        context=super(ViewCrearVenta, self).get_context_data(**kwargs)

        context['suc']=Sucursal.objects.filter(id=self.request.user.sucursal.id)
        return context

class ViewDetalleVenta(DetailView):
    template_name="proces_venta/detalle_venta.html"
    model=Venta
    context_object_name="venta"

    def get_context_data(self, **kwargs):
        context = super(ViewDetalleVenta, self).get_context_data(**kwargs)
        detalle_venta=DetalleVenta.objects.filter(factura__id=self.kwargs['pk'])
        context['detalle_venta']=detalle_venta
        return context

class ListarVentas(ListView):
    template_name="proces_venta/listar_venta.html"
    model=Venta
    context_object_name="ventas"

def obtener_productos_inventario_autocomplete(request):
    id_sucursal=request.POST.get('id_sucursal')
    clave=request.POST.get('term').strip()
    sucursal_user=Sucursal.objects.get(id=id_sucursal)
    productos_buscado=None
    print(request.POST)
    datos=[]
    if clave is not None:
        productos_por_sucursal=ProductoStockSucursal.objects.filter(Q(inventario_productos__sucursal=sucursal_user))
        productos_buscado=productos_por_sucursal.filter(Q(producto__nombre_producto__icontains=clave) | Q(presentacion__presentacion__icontains=clave))
    else:
        if sucursal_user is not None:
            productos_buscado=ProductoStockSucursal.objects.filter(Q(inventario_productos__sucursal=sucursal_user))
    
    for producto_ubi in productos_buscado:
        datos.append(str(producto_ubi.id)+'|'+str(producto_ubi.producto.nombre_producto)+'|'+str(producto_ubi.presentacion.presentacion))

    return JsonResponse(datos, safe=False)

def agregar_producto_detalle_venta(request):
    id_producto_stock_ubicacion=request.POST.get('id_prod_stock')
    producto_stock_ubi=ProductoStockSucursal.objects.get(id=id_producto_stock_ubicacion)
    fila="<tr>"
    fila+="<td><input class='form-control id_prod_stock' value='"+str(producto_stock_ubi.id)+"' disabled></td>"
    fila+="<td><input class='form-control' value='"+str(producto_stock_ubi.producto)+"' disabled></td>"
    fila+="<td><input class='form-control' value='"+str(producto_stock_ubi.presentacion)+"' disabled></td>"
    fila+="<td><input class='form-control cant' value='1'></td>"
    fila+="<td><input class='form-control pre' value='$"+str(producto_stock_ubi.precio)+"' disabled></td>"
    fila+="<td><input class='form-control tot' value='$"+str(producto_stock_ubi.precio)+"' disabled></td>"
    fila+="<td><input class='btn btn-danger form-control delfila' type='button' value='Eliminar'></td>"
    fila+="</tr>"

    datos={
        'fila_producto':fila,
    }
    return JsonResponse(datos, safe=False)

def efectuar_venta(request):
    res=False
    id_sucursal=request.POST.get('id_sucursal')
    sucursal=Sucursal.objects.get(id=id_sucursal)
    no_factura=request.POST.get('numero_factura')
    total_iva=request.POST.get('total_iva')
    total_sin_iva=request.POST.get('total_sin_iva')
    total=request.POST.get('total')
    destalles_de_ventas=json.loads(request.POST.get('detalles_de_facturas'))
    factura_objeto=Venta.objects.get_or_create(usuario=request.user, 
                                        numero_factura=no_factura,
                                        sucursal=sucursal,
                                        total_iva=total_iva,
                                        total_sin_iva=total_sin_iva,
                                        total_con_iva=total
                                      )
    factura=factura_objeto[0]
    resutado_venta=factura_objeto[1]
    cuenta_prod=0
    print(factura_objeto)
    if(resutado_venta==True):
        for prod_stock in destalles_de_ventas:
            id_prod_stock=prod_stock['id_prod_stock']
            producto_stock=ProductoStockSucursal.objects.get(id=id_prod_stock)
            cantidad=prod_stock['cantidad']
            precio=prod_stock['precio']
            total=prod_stock['total']
            DetalleVenta.objects.create(
                factura=factura,
                producto_stock=producto_stock,
                cantidad=cantidad,
                precio=precio,
                total=total
            )
            cuenta_prod=cuenta_prod+1
        if cuenta_prod==len(destalles_de_ventas):
            res=True
    
    return JsonResponse({'res':res})
