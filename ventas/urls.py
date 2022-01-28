from unicodedata import name
from django.urls import path
from .views import Index
from .views import ListarUsuarios, CrearUsuario, EditarUsuario, EliminarUsuario

app_name="store"
urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('usuarios/', ListarUsuarios.as_view(), name="user"),
    path('usuarios/crear_usuarios', CrearUsuario.as_view(), name="crear_user"),
    path('usuarios/editar_usuario/<int:pk>', EditarUsuario.as_view(), name="editar_user"),
    path('usuarios/eliminar_usuario/<int:pk>', EliminarUsuario.as_view(), name="del_user")
]