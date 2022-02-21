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
    
    let url_list_descarga_prod = $("#url_list_prod_a_descargar").val();//url de la lista de productos a descargar
    let csrftoken = getCookie('csrftoken');
    $("#producto").autocomplete({
        source:function(request, response){
            $.ajax({
                url:url_list_descarga_prod,
                type:"POST",
                data:{
                    csrfmiddlewaretoken:csrftoken,
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
            let array_producto=producto.split('|');
            id_prod_stock=array_producto[0];
            agregar_producto_a_descargar_detalle(id_prod_stock);

        }
    });  
    
    function agregar_producto_a_descargar_detalle(id_producto){
        const csrftoken=getCookie('csrftoken');
        let url_add_prod_a_descarga=$("#url_add_prod_a_descarga").val();
        let datos={
            csrfmiddlewaretoken:csrftoken,
            'id_prod_stock':id_producto,
        };
        $.ajax({
            url:url_add_prod_a_descarga,
            type:'POST',
            data:datos,
            dataType:'json',
            success:function(data){
                let fila_producto=data.fila_producto
                $("#table-productos-descarga").prepend(fila_producto)
                $("#producto").val("");
            }
        });
    }

    $(document).on('keyup', '.cant', function(evt){
        let cantidad=parseInt($(this).val());//obteniendo la cantidad ingresada
        let costo=$(this).closest('tr').find('.cost').val().replace('$', '');
        console.log(costo);
        if(!isNaN(cantidad)){
            let total = cantidad*parseFloat(costo)
            if(!isNaN(total)){
                $(this).closest('tr').find('.tot').val("$"+redondear(total));
            }            
        }else{
            $(this).val("0");
            $(this).closest('tr').find('.tot').val("$0.0");
        }
        calcular_totales();
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

    function calcular_totales(){
        let total=0;
        $("#table-productos-descarga tr").each(function(index){
            let cantidad_str=$(this).find(".cant").val();
            let costo_str=$(this).find('.cost').val();
            let cantidad=0;
            let costo=0;
            if(cantidad_str!=''){
                cantidad=parseInt(cantidad_str);
            }
            if(costo_str!=''){
                costo=parseFloat(costo_str.replace('$', ''));
            }
            total+=(cantidad*costo);
        });
        $("#total").text("$"+redondear(total))
    }

});