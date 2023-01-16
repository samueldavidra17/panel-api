from rest_framework import routers
from .api import *
from knox import views as knox_views
from django.urls import path

#Toda la data proviene de api.py
#El default router crea una vista para así visualizar como va la apí
router = routers.DefaultRouter()

router.register('tiposequipos', TiposEquiposViewSet , 'tipos_equipos')
router.register('empresas', EmpresasViewSet , 'empresas')
router.register('departamentos', DepartamentosViewSet , 'departamentos')
router.register('usuarios', UsuariosViewSet , 'usuarios')
router.register('ubicaciones', UbicacionesViewSet , 'ubicaciones')
router.register('estado', EstadosViewSet , 'estado')
router.register('marcas', MarcasViewSet , 'marcas')
router.register('modelos', ModelosViewSet , 'modelos')
router.register('dispositivos', DispositivosViewSet , 'dispositivos')
router.register('impresoras', ImpresorasViewSet , 'impresoras')
router.register('equipos', EquiposViewSet, 'equipos')
router.register('historialequipos', HistorialEquiposViewSet, 'historialEquipos')
router.register('asignaciones', AsignacionesViewSet, 'asignaciones')
router.register('tiposram', TiposRamViewSet, 'tiposram')
router.register('estatus', EstatusViewSet, 'estatus')
router.register('sistemasoperativos', SoViewSet, 'so')
router.register('combox', TextComboxApi, 'combox')
#urls que vienen directamente de django-rest-knox
urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall')
]

urlpatterns += router.urls