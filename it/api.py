from .models import empresas, marcas, tipos_equipos, departamentos, ubicaciones, usuarios, informacion, modelos, equipos, impresoras, dispositivos
from rest_framework import viewsets, permissions, filters, generics
from .serializers import tipos_equiposSerializers, LoginSerializer, equiposSerializers, impresorasSerializers, dispositivosSerializers, modelosSerializers, marcasSerializers, informacionSerializers, ubicacionesSerializers, usuariosSerializers, departamentoSerializers, empresasSerializers, historialSerializers, UserSerializer, RegisterSerializer
import django_filters.rest_framework
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from jSon.models import asignaciones, tiposRam, so, estatus
from jSon.serializers import asignacionesSerializers, estatusSerializers, tiposRamSerializers, soSerializers, asignacionesMinSerializers, estatusMinSerializers, tiposRamMinSerializers, soMinSerializers
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

#ObjectMultipleModel viene de una libreria llamada multiple model 
class TextComboxApi(ObjectMultipleModelAPIViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def get_querylist(self):
        querylist = (
            {'queryset': asignaciones.objects.all(), 'serializer_class': asignacionesMinSerializers},
            {'queryset': estatus.objects.all(), 'serializer_class': estatusMinSerializers},
            {'queryset': tiposRam.objects.all(), 'serializer_class': tiposRamMinSerializers},
            {'queryset': so.objects.all(), 'serializer_class': soMinSerializers},
        )
        return querylist

class asignacionesViewSet(viewsets.ModelViewSet):
    queryset = asignaciones.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = asignacionesSerializers

class tiposRamViewSet(viewsets.ModelViewSet):
    queryset = tiposRam.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = tiposRamSerializers

class estatusViewSet(viewsets.ModelViewSet):
    queryset = estatus.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = estatusSerializers

class soViewSet(viewsets.ModelViewSet):
    queryset = so.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = soSerializers

class tipos_equiposViewSet(viewsets.ModelViewSet):
    queryset = tipos_equipos.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = tipos_equiposSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['marcas']
    search_fields = ['id']

class historialEquiposViewSet(viewsets.ModelViewSet):
    queryset = equipos.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = historialSerializers

class equiposViewSet(viewsets.ModelViewSet, GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = equiposSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['serial','serial_cargador','serial_unidad','dd','ram','tipo_ram','csb','antivirus','usuario_so','so']
    filterset_fields = ['usuarios_id']

        
    ### get_queryset sirve para traer todos los objetos de equipo y retornarlos###
    def get_queryset(self):
        queryset = equipos.objects.all()
        return queryset

    def partial_update(self, request, *args, **kwargs):
        print("patch")
        equipo = self.get_object()
        data = request.data
        try:
            usuario = usuarios.objects.get(pk=data["usuarios"])
            equipo.usuarios = usuario
        except KeyError:
            pass 
        equipo.save()
        serializer = equiposSerializers(equipo)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        print("update")
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
        equipo.usuario_so = data.get("usuario_so", equipo.usuario_so)
        equipo.antivirus = data.get("antivirus", equipo.antivirus)

        equipo.save_without_history()
        serializer = equiposSerializers(equipo)    
        return Response(serializer.data)

    def list(self, request):
        queryset = equipos.objects.values('id','empresas_id__nombre','id__ubicaciones__nombre',
        'serial','csb','usuario_so','modelos_id__nombre',
        'modelos_id__tiposEquiposMarcas_id__marcas_id__nombre', 'usuarios_id',
        'usuarios_id__nombre', 
        'usuarios_id__departamentosEmpresas_id__departamentos_id__nombre',
        'modelos_id__tiposEquiposMarcas_id__tiposEquipos_id__nombre',
        'empresas_id__id')
        search = request.query_params.get('search', None)

        ###Filtros hechos a mano donde startwith se refiere a la letra inicial###
        if search:
            queryset=queryset.filter(
            Q(serial__startswith = search.upper()) |
            Q(empresas_id__nombre__startswith = search.upper()) |
            Q(id__ubicaciones__nombre__startswith = search.upper()) |
            Q(csb__startswith = search.upper()) |
            Q(usuario_so__startswith = search.upper()) |
            Q(modelos_id__nombre__startswith = search.upper()) |
            Q(modelos_id__tiposEquiposMarcas_id__marcas_id__nombre__startswith = search.upper()) |
            Q(usuarios_id__nombre__startswith = search.upper()) 
            ) 


        ###Paginacion###
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = equiposSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = equiposSerializers(queryset, many=True)
        return Response(serializer.data)

class impresorasViewSet(viewsets.ModelViewSet):
    queryset = impresoras.objects.all()
    permission_classes = [permissions.IsAuthenticated | IsUser]
    serializer_class = impresorasSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = []

class dispositivosViewSet(viewsets.ModelViewSet):
    queryset = dispositivos.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = dispositivosSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ["modelos__tiposEquiposMarcas_id__tiposEquipos_id__nombre"]


class modelosViewSet(viewsets.ModelViewSet):
    queryset = modelos.objects.all()
    serializer_class = modelosSerializers
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['id','nombre','tiposEquiposMarcas_id__tiposEquipos_id', 'tiposEquiposMarcas_id__marcas_id']
    

class marcasViewSet(viewsets.ModelViewSet):
    queryset = marcas.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = marcasSerializers
    filter_backends = [filters.SearchFilter,django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['tiposEquiposMarcas']
    search_fields = ['tiposEquiposMarcas__id']

class informacionViewSet(viewsets.ModelViewSet):
    queryset = informacion.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = informacionSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['asignacion']

class ubicacionesViewSet(viewsets.ModelViewSet):
    queryset = ubicaciones.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = ubicacionesSerializers

class usuariosViewSet(viewsets.ModelViewSet):
    queryset = usuarios.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = usuariosSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class departamentosViewSet(viewsets.ModelViewSet):
    queryset = departamentos.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = departamentoSerializers
    filter_backends = [filters.SearchFilter,django_filters.rest_framework.DjangoFilterBackend]
    search_fields = []
    filterset_fields = ['empresas']

class empresasViewSet(viewsets.ModelViewSet):
    queryset = empresas.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = empresasSerializers    
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['id']
