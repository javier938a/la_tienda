from datetime import timezone
from django_weasyprint.utils import django_url_fetcher
import functools
import ssl


from django.conf import settings
from django.views.generic import DetailView, ListView, TemplateView
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from ventas.models import Venta

from django.db.models import Sum

class ViewSelectReporteVentas(TemplateView):
    template_name="reportes/view_select_reporte_ventas.html"

class DetalleReporteVentas(ListView):
    template_name="reportes/reporte_ventas.html"


class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    def get_url_fetcher(self):
        context=ssl.create_default_context()
        context.check_hostname=False
        context.verify_mode=ssl.CERT_NONE
        return functools.partial(django_url_fetcher, ssl_context=context)

class PrintViewReporteVentas(WeasyTemplateResponseMixin, DetalleReporteVentas):
    model=Venta
    context_object_name='ventas'
    
    pdf_stylesheets=[
        str(settings.STATIC_ROOT) + '/assets/css/estilos_reporte_venta/reporte_venta.css',
    ]
    
    pdf_attachment=False
    
    response_class=CustomWeasyTemplateResponse

    def get_context_data(self, **kwargs):
        context=super(PrintViewReporteVentas, self).get_context_data(**kwargs)
        fecha_inicial=self.request.GET['fecha_inicial']
        fecha_final=self.request.GET['fecha_final']
        context['fecha_inicial']=fecha_inicial
        context['fecha_final']=fecha_final
        todas_las_ventas=Venta.objects.filter(fecha_venta__range=[fecha_inicial, fecha_final])
        total_iva_sum_dic=todas_las_ventas.aggregate(Sum('total_iva'))#obteniendo la suma total del iva
        total_sin_iva_dic=todas_las_ventas.aggregate(Sum('total_sin_iva'))#obteniendo la suma total sin iva
        total_sin_iva=total_sin_iva_dic['total_sin_iva__sum']
        total_iva=total_iva_sum_dic['total_iva__sum']
        total_con_iva_dic=todas_las_ventas.aggregate(Sum('total_con_iva'))##obteniendo la suma de el total del total con iva
        total_con_iva=total_con_iva_dic['total_con_iva__sum']
        
        context['total_iva_sum']=round(total_iva, 2)
        context['total_sin_iva_sum']=round(total_sin_iva, 2)
        context['total_con_iva_sum']= round(total_con_iva, 2)
        return context

    def get_queryset(self):
        fecha_inicial=self.request.GET['fecha_inicial']
        fecha_final=self.request.GET['fecha_final']
        lista_de_ventas=self.model.objects.filter(fecha_venta__range=[fecha_inicial, fecha_final])
        return lista_de_ventas

class DownloadView(WeasyTemplateResponseMixin, DetalleReporteVentas):
    pdf_filename="reporte_venta.pdf"

class DynamicNameView(WeasyTemplateResponseMixin, DetalleReporteVentas):
    def get_pdf_filename(self):
        return 'foo-{at}.pdf'.format(
            at=timezone.now().strftime('%Y%m%d-%H%M'),
        )



