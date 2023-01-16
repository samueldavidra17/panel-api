from .models import *
from .serializers import *
from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import django_filters.rest_framework
from django.db.models import Q
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission
from knox.models import AuthToken  

# DOCUMENTACION

# Todos los serializer provienen de serializers.py de la carpeta it

# permissions hace referencia a la permisologia para acceder a cada tabla. es decir
# que el usuario debe estar registrado

#Filter hace referencia a los filtros dentro de cada vista

# Register API
# Proviene de django-rest-knox, investigar para conocer más
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(generics.GenericAPIView):
  serializer_class = LoginSerializer
  permission_classes = [permissions.AllowAny]

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    _, token = AuthToken.objects.create(user)
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": token
    })

class IsUser(BasePermission):
   def has_permission(self, request, view, read_only=True):
      return request.user
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class EmpresasViewSet(viewsets.ModelViewSet):
    queryset = Empresas.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmpresasSerializers    
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['id']

class DepartamentosViewSet(viewsets.ModelViewSet):
    queryset = Departamentos.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = DepartamentoSerializers
    filter_backends = [filters.SearchFilter,django_filters.rest_framework.DjangoFilterBackend]
    search_fields = []
    filterset_fields = ['empresas']

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = UsuarioSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']    

class TiposEquiposViewSet(viewsets.ModelViewSet):
    queryset = TiposEquipos.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TiposEquipoSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['marcas']
    search_fields = ['id']

class MarcasViewSet(viewsets.ModelViewSet):
    queryset = Marcas.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = MarcaSerializers
    filter_backends = [filters.SearchFilter,django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['tiposEquiposMarcas']
    search_fields = ['tiposEquiposMarcas__id']

class ModelosViewSet(viewsets.ModelViewSet):
    queryset = Modelos.objects.all()
    serializer_class = ModeloSerializers
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['id','nombre','tiposEquiposMarcas_id__tiposEquipos_id', 'tiposEquiposMarcas_id__marcas_id']

class UbicacionesViewSet(viewsets.ModelViewSet):
    queryset = Ubicaciones.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = UbicacioneSerializers

class AsignacionesViewSet(viewsets.ModelViewSet):
    queryset = Asignaciones.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AsignacioneSerializers

class EstatusViewSet(viewsets.ModelViewSet):
    queryset = Estatus.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EstatuSerializers

class EstadosViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = EstadoSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['asignacion']

class TiposRamViewSet(viewsets.ModelViewSet):
    queryset = TiposRam.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TiposRamSerializers

class SoViewSet(viewsets.ModelViewSet):
    queryset = So.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SoSerializers

class EquiposViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EquipoSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['serial','serial_cargador','serial_unidad','dd','ram','tipo_ram','csb','antivirus','nombre','so']
    filterset_fields = ['usuario_id']

    ### get_queryset sirve para traer todos los objetos de equipo y retornarlos###
    def get_queryset(self):
        queryset = Equipos.objects.all()
        return queryset

    def partial_update(self, request, *args, **kwargs):
        equipo = self.get_object()
        data = request.data
        try:
            print(data)
            usuario = Usuarios.objects.get(pk=data["usuario"])
            equipo.usuario = usuario
            equipo.save()
            serializer = EquipoSerializers(equipo)
            return Response(serializer.data)
        except KeyError:
            pass 

    def update(self, request, *args, **kwargs):
        equipo = self.get_object()
        data = request.data
        
        equipo.serial = data.get("serial", equipo.serial)
        equipo.serial_cargador = data.get("serial_cargador", equipo.serial_cargador)
        equipo.serial_unidad = data.get("serial_unidad", equipo.serial_unidad)
        equipo.so = data.get("so", equipo.so)
        equipo.csb = data.get("csb", equipo.csb)
        equipo.dd = data.get("dd", equipo.dd)
        equipo.ram = data.get("ram", equipo.ram)
        equipo.tipo_ram = data.get("tipo_ram", equipo.tipo_ram)
        equipo.nombre = data.get("nombre", equipo.nombre)
        equipo.antivirus = data.get("antivirus", equipo.antivirus)

        equipo.save_without_history()
        serializer = EquipoSerializers(equipo)    
        return Response(serializer.data)

    def list(self, request):
        queryset = Equipos.objects.values('id','empresas_id__nombre','id__ubicaciones__nombre',
        'serial','csb','nombre','modelo_id__nombre',
        'modelo_id__tiposEquiposMarcas_id__marcas_id__nombre', 'usuario_id',
        'usuario_id__nombre', 
        'usuario_id__departamentosEmpresas_id__departamentos_id__nombre',
        'modelo_id__tiposEquiposMarcas_id__tiposEquipos_id__nombre',
        'empresas_id__id')
        search = request.query_params.get('search', None)
        ###Filtros hechos a mano donde startwith se refiere a la letra inicial###
        if search:
            queryset=queryset.filter(
            Q(serial__startswith = search.upper()) |
            Q(empresas_id__nombre__startswith = search.upper()) |
            Q(id__ubicaciones__nombre__startswith = search.upper()) |
            Q(csb__startswith = search.upper()) |
            Q(nombre__startswith = search.upper()) |
            Q(modelo_id__nombre__startswith = search.upper()) |
            Q(modelo_id__tiposEquiposMarcas_id__marcas_id__nombre__startswith = search.upper()) |
            Q(usuario_id__nombre__startswith = search.upper()) 
            ) 


        ###Paginacion###
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = EquipoSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = EquipoSerializers(queryset, many=True)
        return Response(serializer.data)

class HistorialEquiposViewSet(viewsets.ModelViewSet):
    queryset = Equipos.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HistorialSerializers

class ImpresorasViewSet(viewsets.ModelViewSet):
    queryset = Impresoras.objects.all()
    permission_classes = [permissions.IsAuthenticated | IsUser]
    serializer_class = ImpresoraSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = []

class DispositivosViewSet(viewsets.ModelViewSet):
    queryset = Dispositivos.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = DispositivoSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ["modelos__tiposEquiposMarcas_id__tiposEquipos_id__nombre"]

#ObjectMultipleModel viene de una libreria llamada multiple model 
class ComboxApi(ObjectMultipleModelAPIViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def get_querylist(self):
        querylist = (
            {'queryset': Asignaciones.objects.all(), 'serializer_class': AsignacioneSerializers},
            {'queryset': Estatus.objects.all(), 'serializer_class': EstatuSerializers},
            {'queryset': TiposRam.objects.all(), 'serializer_class': TiposRamSerializers},
            {'queryset': So.objects.all(), 'serializer_class': SoSerializers},
        )
        return querylist

class PowerBIApi(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):
        queryset = Equipos.objects.all()
        serializer = PowerBISerializers(queryset, many=True)
        return Response(serializer.data)
