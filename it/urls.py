from rest_framework import routers
from .api import tipos_equiposViewSet, dispositivosViewSet, empresasViewSet, departamentosViewSet, usuariosViewSet, ubicacionesViewSet, informacionViewSet, marcasViewSet, modelosViewSet, impresorasViewSet, equiposViewSet, asignacionesViewSet, tiposRamViewSet, estatusViewSet, soViewSet, TextComboxApi, historialEquiposViewSet, RegisterAPI, LoginAPI
from knox import views as knox_views
from django.urls import path

#Toda la data proviene de api.py
#El default router crea una vista para así visualizar como va la apí
router = routers.DefaultRouter()

router.register('api/tiposequipos', tipos_equiposViewSet , 'tipos_equipos')
router.register('api/empresas', empresasViewSet , 'empresas')
router.register('api/departamentos', departamentosViewSet , 'departamentos')
router.register('api/usuarios', usuariosViewSet , 'usuarios')
router.register('api/ubicaciones', ubicacionesViewSet , 'ubicaciones')
router.register('api/informacion', informacionViewSet , 'informacion')
router.register('api/marcas', marcasViewSet , 'marcas')
router.register('api/modelos', modelosViewSet , 'modelos')
router.register('api/dispositivos', dispositivosViewSet , 'dispositivos')
router.register('api/impresoras', impresorasViewSet , 'impresoras')
router.register('api/equipos', equiposViewSet, 'equipos')
router.register('api/historialequipos', historialEquiposViewSet, 'historialEquipos')
router.register('api/asignaciones', asignacionesViewSet, 'asignaciones')
router.register('api/tiposram', tiposRamViewSet, 'tiposram')
router.register('api/estatus', estatusViewSet, 'estatus')
router.register('api/sistemasoperativos', soViewSet, 'so')
router.register('api/combox', TextComboxApi, 'combox')

#urls que vienen directamente de django-rest-knox
urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall')
]

urlpatterns += router.urls
