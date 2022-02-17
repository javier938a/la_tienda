from multiprocessing.sharedctypes import Value
import profile
from django.views.generic import ListView, TemplateView, DetailView
from ventas.models import Venta, DetalleVenta, Sucursal, ProductoStockSucursal, User
from django.db.models import Q
from django.http import JsonResponse
from django.core.serializers import serialize
import json

from escpos.printer import Usb

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
    fila=""
    existencia=producto_stock_ubi.cantidad#obtenemos la existencia del producto
    res=False#esta variable confirmara si hay existencia si es False es porque no hay en existencia si cambia True es porque hay en existencia
    if int(existencia)>0:#si es mayor que cero se crea la fila con sus valores y por defencto con cantidad 1
        fila="<tr>"
        fila+="<td><input class='form-control id_prod_stock' value='"+str(producto_stock_ubi.id)+"' disabled></td>"
        fila+="<td><input class='form-control' value='"+str(producto_stock_ubi.producto)+"' disabled></td>"
        fila+="<td><input class='form-control' value='"+str(producto_stock_ubi.presentacion)+"' disabled></td>"
        fila+="<td><input class='form-control cant' value='1'></td>"
        fila+="<td><input class='form-control pre' value='$"+str(producto_stock_ubi.precio)+"' disabled></td>"
        fila+="<td><input class='form-control tot' value='$"+str(producto_stock_ubi.precio)+"' disabled></td>"
        fila+="<td><input class='btn btn-danger form-control delfila' type='button' value='Eliminar'></td>"
        fila+="</tr>"
        res=True

    datos={
        'res':res,
        'fila_producto':fila,
    }
    return JsonResponse(datos, safe=False)

def verificar_stock_producto(request):
    id_prod_stock=request.POST.get('id_prod_stock')
    producto_stock=ProductoStockSucursal.objects.get(id=id_prod_stock)
    cantidad_real=producto_stock.cantidad
    datos={
        'cantidad_real':cantidad_real,
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
            #cuando la venta de un producto se efectua se debe de alterar el stock restandole la cantidad que se vende
            nueva_cantidad_disponible=int(producto_stock.cantidad)-int(cantidad)
            costo_producto_stock=float(producto_stock.costo)
            nuevo_total_inventario=nueva_cantidad_disponible*costo_producto_stock
            #teniendo la cantidad disponible se actualiza el producto_stock_ubicacion
            ProductoStockSucursal.objects.filter(id=id_prod_stock).update(
                cantidad=nueva_cantidad_disponible,
                total=nuevo_total_inventario
            )
            cuenta_prod=cuenta_prod+1
            if cuenta_prod==len(destalles_de_ventas):
                res=True
            datos=None
            if res==True:#si se registran bien todos los detalles de facturas pasara a generarse el contenido del ticket
                ##obteniendo todos los datos registrados para devolverlos ya que con ellos se formara la factura o en este caso el ticket##
                ticket=obtener_datos_factura(factura.id)
                datos={
                    'res':res,
                    'datos_factura':ticket
                }
            
        
    return JsonResponse(datos, safe=False)

def obtener_datos_factura(id_venta):
    factura=Venta.objects.get(id=id_venta)

    detalle_factura=DetalleVenta.objects.filter(factura=factura)
    detalles_de_factura=[]
    for detalle in detalle_factura:
        fila={
            'producto':str(detalle.producto_stock.producto), 
            'presentacion':str(detalle.producto_stock.presentacion),
            'cantidad':str(detalle.cantidad), 
            'precio':str(detalle.precio), 
            'total':str(detalle.total)
        }
        detalles_de_factura.append(fila)
    ticket={
            'factura':{
            'fecha_venta':str(factura.fecha_venta),
            'cajero':str(factura.usuario),
            'numero_factura':str(factura.numero_factura),
            'sucursal':str(factura.sucursal),
            'total_iva':str(factura.total_iva),
            'total_sin_iva':str(factura.total_sin_iva),
            'total_con_iva':str(factura.total_con_iva)
        },
            'detalle_de_factura':json.dumps(detalles_de_factura)
     }
    return ticket


def Obtener_ticket(request):
    id_venta=request.POST.get('id_venta')
    res=True
    ticket=None
    try:
        ticket=obtener_datos_factura(id_venta)
    except ValueError:
        print(ValueError.__name__)
        res=False

    

    return JsonResponse({
        'res':res,
        'datos_ticket':ticket
    }, safe=False)

#funcion para solo imprimir los datos
def imprimir_ticket(request):
    id_venta=request.POST.get('id_venta')
    #primero darle permiso al puerto lp0 si es necesario...
    #chmod +777 /dev/usb/lp0
    #en linux buscar la impresora entre todos los dispositivos que lista el comando 'lsusb'
    #los parametros son el idVendor y el idProduc
    #la informacion de esos dos estan despues del ID
    #tira esto
    #Bus 001 Device 008: ID 0483:5743 STMicroelectronics
    #ID idVendor:idProduc
    #en los parametros se colocan como 0xidVendor, 0xidProduct
    #0483:5743
    print(id_venta)
    impresora=Usb(0x0483,0x5743, 0)
    impresora.text("Este es un texto de prueba\n")
    impresora.qr('You can readme from your smartphone')
    impresora.cut()
    return JsonResponse({'res':True})
