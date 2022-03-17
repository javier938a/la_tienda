$(document).ready(function(){
    $("#fecha_inicio").datepicker({
        dateFormat:'yy-mm-dd',
    });
    $("#fecha_inicio").mask('0000-00-00');

    $("#fecha_final").datepicker({
        dateFormat:'yy-mm-dd',
    });
    $("#fecha_final").mask('0000-00-00');
    //generando el reporte

})