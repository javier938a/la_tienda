import imp
import json
from math import prod
from multiprocessing import context
from pyexpat import model
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from ventas.models import InventarioProductos, Sucursal, Producto, Presentacion, User, ProductoStockSucursal
from django.http import request, JsonResponse
from django.db.models import Q
from django.core.serializers import serialize

class CrearInventario(TemplateView):
    template_name="proces_inventario/crear_inventario.html"
    def get_context_data(self, **kwargs) :
        context=super(CrearInventario, self).get_context_data()
        sucursales=Sucursal.objects.all()
        context['suc']=sucursales
        return context

class EditarInventario(TemplateView):
    pass

class EliminarInventario(TemplateView):
    pass

class ListarInventario(ListView):
    template_name="proces_inventario/listar_inventario.html"
    model=InventarioProductos
    context_object_name="inventario"


def obtener_productos_autocomplete(request):
    clave=request.POST.get('clave')
    productos=None
    datos=[]
    if clave is not None:
        productos=Producto.objects.filter(Q(nombre_producto__icontains=clave))
        for prod in productos:
            datos.append(str(prod.pk)+'|'+str(prod.descripcion))
    else:
        productos=Producto.objects.all()
        for prod in productos:
            datos.append(str(prod.pk)+'|'+str(prod.descripcion))
    return JsonResponse(datos, safe=False)

def agregar_producto_detalle(request):
    id_producto=request.POST.get('id_producto')
    producto=Producto.objects.get(pk=id_producto)
    presentaciones=Presentacion.objects.all()
    fila_producto='<tr>'
    fila_producto+='<td><input class="form-control idprod" type="text" value="'+str(id_producto)+'" disabled></td>'
    fila_producto+='<td><input class="form-control" type="text" value="'+str(producto.nombre_producto)+'" disabled></td>'
    fila_producto+='<td>'+obtener_presentaciones(presentaciones)+'</td>'
    fila_producto+='<td><input class="form-control cant" type="text" value=""></td>'
    fila_producto+='<td><input class="form-control cost" type="text" value=""></td>'
    fila_producto+='<td><input class="form-control pre" type="text" value=""></td>'
    fila_producto+='<td><input class="form-control tot" type="text" value="" disabled></td>'
    fila_producto+='<td><i class="fas fa-trash"></i></td>'
    fila_producto+='<td><input class="btn btn-danger form-control delfila" type="button" value="Eliminar"></td>'
    fila_producto+='</tr>'

    datos={
        'fila_producto':fila_producto
    }
    return JsonResponse(datos, safe=False)
    

def obtener_presentaciones(presentaciones):
    sel='<select class="form-control select">'
    sel+='<option value="">Seleccione</option>'
    for pre in presentaciones:
        sel+='<option value="'+str(pre.pk)+'">'+str(pre.presentacion)+'</option>'
    
    sel+="</select>"
    return sel

def guardar_datos_inventario(request):
    descripcion=request.POST.get('descripcion')
    id_sucursal=request.POST.get('id_sucursal')
    total=request.POST.get('total')
    productos_json= json.loads(request.POST.get('productos_json'))
    #obteniendo el usuario
    user=User.objects.get(id=request.user.id)#obteniendo el usuario que esta loguiado en el sistema
    #obteniendo la sucursal
    sucursal=Sucursal.objects.get(id=id_sucursal)#obteniendo la sucursal a donde se almacenaran los productos
    crear_inv=InventarioProductos.objects.get_or_create(usuario=user, descripcion=descripcion, sucursal=sucursal, total=total)
    inventario=crear_inv[0]
    #una vez creado el inventario se registrar los detalles del inventario ya que es necesario para crearlo
    cuenta_res=0
    res=False
    for prod in productos_json:
        producto=Producto.objects.get(id=prod['id_producto'])
        presentacion=Presentacion.objects.get(id=prod['id_presentacion'])
        cantidad=prod['cantidad']
        costo=prod['costo']
        precio=prod['precio']
        total=prod['total']
        ProductoStockSucursal.objects.create(
            inventario_productos=inventario, 
            producto=producto, 
            presentacion=presentacion, 
            cantidad=cantidad, 
            costo=costo, 
            precio=precio, 
            total=total
        )
        cuenta_res=cuenta_res+1
    
    if(cuenta_res==len(productos_json)):
        res=True



    return JsonResponse({'res':res,}, safe=False)


    
