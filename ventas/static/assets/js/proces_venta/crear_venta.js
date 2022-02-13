function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
    $("#sucursal").select2();

    let url_inv_autocomplete=$("#url_productos_inv_autocomplete").val();
    const csrftoken=getCookie('csrftoken');
    let id_sucursal=$("#sucursal").val();


    $("#producto").autocomplete({
        source:function(request, response){
            $.ajax({
                url:url_inv_autocomplete,
                type:"POST",
                data:{
                    csrfmiddlewaretoken:csrftoken,
                    'id_sucursal':id_sucursal,
                    term:request.term
                },
                dataType:'json',
                success:function(data){
                    response(data)
                }
            })
        },
        minLength:2,
        select:function(event, ui){
            let producto=ui.item.value;
            let prod_array=producto.split('|');
            id_prod_stock=prod_array[0];
            console.log(producto);
            agregar_producto_detalle_venta(id_prod_stock);

        }
    });

    function agregar_producto_detalle_venta(id_prod_stock){
        let url_add_prod_venta=$('#url_add_prod_venta').val();
        const csrftoken=getCookie('csrftoken');
        datos={
            csrfmiddlewaretoken:csrftoken,
            'id_prod_stock':id_prod_stock
        }
        $.ajax({
            url:url_add_prod_venta,
            type:'POST',
            data:datos,
            dataType:'json',
            success:function(data){
                let fila_producto=data.fila_producto;
                console.log(fila_producto);
                $("#table-productos-venta").prepend(fila_producto);
                $("#producto").val("");
                calcular_totales();
            }
        })
    }

    $(document).on('input', '.cant', function(){
        this.value=this.value.replace(/[^0-9]/g,'');
    });
    
    $(document).on('click', '.delfila', function(){
        let fila = $(this).parents('tr');
        fila.remove();
        calcular_totales();
    });
    //funcion para redondear cantidades a dos digitos
    function redondear(num) {
        var m = Number((Math.abs(num) * 100).toPrecision(15));
        return Math.round(m) / 100 * Math.sign(num);
    }
    $(document).on('keyup', '.cant', function(){//obteniendo el evento de cada una de las celdas en donde se ingresa la cantidad
        let cantidad= parseInt($(this).val());//obteniendo el total que se esta ingresando
        let precio=$(this).closest('tr').find('.pre').val().replace('$', '');//obtenendo el costo que esta en el canpo costo no se convierte porque pueda quee este vacio
                                        //closest devuelve el primer antecesor del elemento
        if(!isNaN(cantidad)){//si el el campo costo no esta vacio multiplica el costo por el total
            let total=cantidad*parseFloat(precio);
            $(this).closest('tr').find('.tot').val('$'+redondear(total));//se asigna el total campo del total
        }else{
            $(this).closest('tr').find('.tot').val("$0.0");//de lo contrario el input del total sera vacio
        }
        calcular_totales();
    });

    function calcular_totales(){
        let total=0;
        $("#table-productos-venta tr").each(function(){
            let cantidad_str=$(this).find(".cant").val();
            let precio_str=$(this).find(".pre").val();
            let cantidad=0;
            let precio=0;
        
            if(cantidad_str!=''){
                cantidad=parseInt(cantidad_str);
            }
            if(precio_str!=''){
                precio=parseFloat(precio_str.replace("$",''));
            }
            total+=(cantidad*precio);
        });
        console.log(total)
        let total_iva= redondear(total*0.13);
        $("#total_iva").text("$"+total_iva);
        //aqui iria el total sin iva
        $("#total_sin_iva").text("$"+total);
        let total_con_iva=total_iva+redondear(total);
        $("#total").text("$"+ redondear(total_con_iva));
    }

    $("#efectuar_venta").click(function(evt){
        console.log("Hola");
        let no_documento=$("#no_documento").val();
        console.log(no_documento.length);
        if(no_documento.length>0){            
            let detalles_venta_prod=$("#table-productos-venta tr");
            let res_validad_detalles=validar_detalles_ventas(detalles_venta_prod);
            if(res_validad_detalles==false){///si resultado es igual false entonces es porque todos los campos de ingresar cantidades es correcto y hay al menos un producto ingresado
                const csrftoken=getCookie("csrftoken");
                let detalles_de_facturas=obtener_detalles_productos(detalles_venta_prod);
                let numero_factura=$("#no_documento").val();
                let total_iva=$("#total_iva").text().replace('$','');
                let total_sin_iva=$("#total_sin_iva").text().replace('$', '');
                let total=$("#total").text().replace('$','');         
                let id_sucursal=$("#sucursal").val();
                let datos={
                    csrfmiddlewaretoken:csrftoken,
                    'numero_factura':numero_factura,
                    'id_sucursal':id_sucursal,
                    'total_iva':total_iva,
                    'total_sin_iva':total_sin_iva,
                    'total':total,
                    'detalles_de_facturas':JSON.stringify(detalles_de_facturas),
               }
               url_efectuar_venta=$("#url_efectuar_venta").val();
               $.ajax({
                    url:url_efectuar_venta,
                    type:'POST',
                    data:datos,
                    dataType:'json',
                    success:function(data){
                        let resultado=data.res;
                        if(resultado){
                            toastr['success']("Venta registrada exitosamente");
                            ///aqui el codigo que imprimira el ticket e redireccionara al listado de ventas
                        }else{
                            toastr['error']("La Venta no pudo ser registrada exitosamente");
                        }
                    }
               });
            }else{
                toastr['error']("Debe de ingresar al menos un producto y debe de ingresar todas las cantidades de todos los productos ingresados");
            }
        }else{
            toastr['error']("Debe de ingresar un numero de factura");
        }
    });

    function validar_detalles_ventas(tabla_detalle){
        //cuenta que no haya ningun campo de cantidad vacio
        let cuenta_cantidad=0;
        let res=false;//si res cambia a true es porque hay campos de cantidades vacios
        tabla_detalle.each(function(index){
            let cantidad=$(this).find('.cant').val();
            if(cantidad.length===0){
                cuenta_cantidad++;
                console.log("Entro aqui...")
                console.log(cantidad);

            }
        })
        let num_filas=tabla_detalle.length;
        if(cuenta_cantidad>0 || num_filas===0){
            res=true
        }
        
        return res;
    }

    function obtener_detalles_productos(tabla_detalle){
        let datos=[];
        tabla_detalle.each(function(){
            let id_producto_stock=$(this).find('.id_prod_stock').val();
            let cantidad=$(this).find('.cant').val();
            let precio=$(this).find('.pre').val().replace('$','');
            let total=$(this).find('.tot').val().replace('$','');
            fila={'id_prod_stock':id_producto_stock, 'cantidad':cantidad, 'precio':precio, 'total':total};
            datos.push(fila);
        });
        return datos;
    }

    
});