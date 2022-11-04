from .models import empresas, marcas, tipos_equipos, tipos_equipos_marcas, departamentos, ubicaciones, usuarios, informacion, modelos, equipos, impresoras, dispositivos
from rest_framework import viewsets, permissions, filters, status
from .serializers import tipos_equiposSerializers, tipos_equipos_marcasSerializers, equiposSerializers, equiposSerializersMin, impresorasSerializers, dispositivosSerializers, modelosSerializers, marcasSerializers, informacionSerializers, ubicacionesSerializers, usuariosSerializers, departamentoSerializers, empresasSerializers
import django_filters.rest_framework
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class tipos_equiposViewSet(viewsets.ModelViewSet):
    queryset = tipos_equipos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = tipos_equiposSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['marcas']

class tipos_equipos_marcasViewSet(viewsets.ModelViewSet):
    queryset = tipos_equipos_marcas.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = tipos_equipos_marcasSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['marcas_id__nombre','tiposEquipos_id__nombre']

class equiposViewSet(viewsets.ModelViewSet):
    # queryset = equipos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = equiposSerializers
    # pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['serial','serial_cargador','serial_unidad','dd','ram','tipo_ram','csb','tipo_equipo','antivirus','usuario_so','so']
    filterset_fields = ['usuarios_id']
    # http_method_names = ['patch','get']

    def get_queryset(self):
        pass

    def list(self, request):
        queryset = equipos.objects.all().values('id','empresas_id__nombre','id__ubicaciones__nombre',
        'serial','csb','tipo_equipo','usuario_so','modelos_id__nombre',
        'modelos_id__tiposEquiposMarcas_id__marcas_id__nombre', 'usuarios_id',
        'usuarios_id__nombre', 
        'empresas_id__id')
        # queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = equiposSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = equiposSerializers(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # print(kwargs['pk'])
        queryset = equipos.objects.filter(**kwargs)
        serializer = equiposSerializers(queryset, many=True)
        return Response(serializer.data)

class equiposViewSetMin(viewsets.ModelViewSet):
    queryset = equipos.objects.all().values('id','empresas_id__nombre','id__ubicaciones__nombre',
    'serial','csb','tipo_equipo','usuario_so','modelos_id__nombre',
    'modelos_id__tiposEquiposMarcas_id__marcas_id__nombre', 'usuarios_id',
    'usuarios_id__nombre', 
    'empresas_id__id')
    permission_classes = [permissions.AllowAny]
    serializer_class = equiposSerializersMin
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['serial','csb','usuario_so','usuarios_id__nombre']
    filterset_fields = ['usuarios_id']
    # http_method_names = ['patch','get']

    # def list(self, request):
    #     serializer = equiposSerializersMin(self.queryset,many=True,)
    #     return Response (serializer.data)
    
    # def retrieve(self, request, pk=None):
    #     item = get_object_or_404(self.queryset, pk=pk)
    #     serializer = equiposSerializersMin(item)
    #     return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def values(self, request):
        user_count = equipos.objects.all().values()
        return Response(user_count)

class impresorasViewSet(viewsets.ModelViewSet):
    queryset = impresoras.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = impresorasSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = []

class dispositivosViewSet(viewsets.ModelViewSet):
    queryset = dispositivos.objects.all()
    permission_classes = [permissions.AllowAny] 
    serializer_class = dispositivosSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = []


class modelosViewSet(viewsets.ModelViewSet):
    queryset = modelos.objects.all()
    serializer_class = modelosSerializers
    permission_classes = [permissions.AllowAny] 
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['id','nombre', 'tiposEquiposMarcas_id__tiposEquipos_id', 'tiposEquiposMarcas_id__marcas_id']
    

class marcasViewSet(viewsets.ModelViewSet):
    queryset = marcas.objects.all()
    serializer_class = marcasSerializers
    permission_classes = [permissions.AllowAny] 
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['tiposEquiposMarcas']

class informacionViewSet(viewsets.ModelViewSet):
    queryset = informacion.objects.all()
    permission_classes = [permissions.AllowAny] 
    serializer_class = informacionSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['asignacion']

class ubicacionesViewSet(viewsets.ModelViewSet):
    queryset = ubicaciones.objects.all()
    permission_classes = [permissions.AllowAny] 
    serializer_class = ubicacionesSerializers
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_fields = ['empresasforeingkey_id']

class usuariosViewSet(viewsets.ModelViewSet):
    queryset = usuarios.objects.all()
    permission_classes = [permissions.AllowAny] 
    serializer_class = usuariosSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class departamentosViewSet(viewsets.ModelViewSet):
    queryset = departamentos.objects.all()
    permission_classes = [permissions.AllowAny] 
    serializer_class = departamentoSerializers
    filter_backends = [filters.SearchFilter,django_filters.rest_framework.DjangoFilterBackend]
    search_fields = []
    filterset_fields = ['empresas']

class empresasViewSet(viewsets.ModelViewSet):
    queryset = empresas.objects.all()
    permission_classes = [permissions.AllowAny] 
    serializer_class = empresasSerializers    
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['id']