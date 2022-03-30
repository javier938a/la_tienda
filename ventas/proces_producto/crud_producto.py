from multiprocessing import context
from django.urls import reverse_lazy
from ventas.models import Producto, User
from ventas.forms import ProductoForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render
from django.db.models import Count

class CrearProducto(CreateView):
    template_name="proces_producto/crear_producto.html"
    model=Producto
    form_class=ProductoForm
    context_object_name="form"
    success_url=reverse_lazy("store:list_prod")
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context=super(CrearProducto, self).get_context_data(**kwargs)
        context['form'].fields['usuario'].empty_label=None #Eliminando el '------'
        context['form'].fields['usuario'].queryset=User.objects.filter(id=self.request.user.id)#filtrando que solo se muestre el usuario logiado
        return context
    def post(self, request, *args, **kwargs):
        form=self.get_form()#obtiene el formulario del modelo
        if form.is_valid():#si el formulario es valido 
            codigo_barra=form.cleaned_data.get('codigo_barra')
            if Producto.objects.filter(codigo_barra=codigo_barra).exists():#si el codigo de barra ingresado existe debe de llevar hacia esta plantilla
                return render(
                    request,
                    'proces_producto/mensaje_codigo_barra_existente.html'
                )
            else:#de lo contrario se guarda correctamente..
                return self.form_valid(form)#llama al metodo form_valid y le pasamos el formulario
        else:
            return self.form_invalid(form)#de lo contrario retornamos a form_invalid y le pasamos el formulario
        

class EditarProducto(UpdateView):
    template_name="proces_producto/editar_producto.html"
    model=Producto
    form_class=ProductoForm
    context_object_name="form"
    success_url=reverse_lazy("store:list_prod")

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context=super(EditarProducto, self).get_context_data(**kwargs)
        context['form'].fields['usuario'].empty_label=None
        context['form'].fields['usuario'].queryset=User.objects.filter(id=self.request.user.id)
        return context


class EliminarProducto(DeleteView):
    template_name="proces_producto/eliminar_producto.html"
    model=Producto
    context_object_name="prod"
    success_url=reverse_lazy("store:list_prod")

class DetalleProducto(DetailView):
    template_name="proces_producto/detalle_producto.html"
    model=Producto
    context_object_name="prod"

class ListarProductos(ListView):
    template_name="proces_producto/listar_producto.html"
    model=Producto
    context_object_name="producto"

    