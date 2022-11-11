from .models import empresas, marcas, tipos_equipos, tipos_equipos_marcas, departamentos, ubicaciones, usuarios, informacion, modelos, equipos, impresoras, dispositivos
from rest_framework import viewsets, permissions, filters, status, mixins
from .serializers import tipos_equiposSerializers, tipos_equipos_marcasSerializers, equiposSerializers, impresorasSerializers, dispositivosSerializers, modelosSerializers, marcasSerializers, informacionSerializers, ubicacionesSerializers, usuariosSerializers, departamentoSerializers, empresasSerializers
import django_filters.rest_framework
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import Q
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from jSon.models import asignaciones, tiposRam, so, estatus
from jSon.serializers import asignacionesSerializers, estatusSerializers, tiposRamSerializers, soSerializers, asignacionesMinSerializers, estatusMinSerializers, tiposRamMinSerializers, soMinSerializers
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class TextComboxApi(ObjectMultipleModelAPIViewSet):
    def get_querylist(self):
        querylist = (
            {'queryset': asignaciones.objects.using('json_db'), 'serializer_class': asignacionesMinSerializers},
            {'queryset': estatus.objects.using('json_db'), 'serializer_class': estatusMinSerializers},
            {'queryset': tiposRam.objects.using('json_db'), 'serializer_class': tiposRamMinSerializers},
            {'queryset': so.objects.using('json_db'), 'serializer_class': soMinSerializers},
        )
        return querylist

class asignacionesViewSet(viewsets.ModelViewSet):
    queryset = asignaciones.objects.using('json_db')
    permission_classes = [permissions.AllowAny]
    serializer_class = asignacionesSerializers

class tiposRamViewSet(viewsets.ModelViewSet):
    queryset = tiposRam.objects.using('json_db')
    permission_classes = [permissions.AllowAny]
    serializer_class = tiposRamSerializers

class estatusViewSet(viewsets.ModelViewSet):
    queryset = estatus.objects.using('json_db')
    permission_classes = [permissions.AllowAny]
    serializer_class = estatusSerializers

class soViewSet(viewsets.ModelViewSet):
    queryset = so.objects.using('json_db')
    permission_classes = [permissions.AllowAny]
    serializer_class = soSerializers

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

class equiposViewSet(viewsets.ModelViewSet, GenericAPIView):
    # queryset = equipos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = equiposSerializers
    # pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['serial','serial_cargador','serial_unidad','dd','ram','tipo_ram','csb','antivirus','usuario_so','so']
    filterset_fields = ['usuarios_id']
    # http_method_names = ['patch','get']

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid()
    #     self.perform_update(serializer)
    #     return Response(serializer.data)
    # @api_view(['GET'])
    # def get_equipos(request, pk):
    #     print(pk)
        
    def get_queryset(self):
        queryset = equipos.objects.all()
        return queryset

    def list(self, request):
        # print(self.get_queryset)
        queryset = self.get_queryset().values('id','empresas_id__nombre','id__ubicaciones__nombre',
        'serial','csb','usuario_so','modelos_id__nombre',
        'modelos_id__tiposEquiposMarcas_id__marcas_id__nombre', 'usuarios_id',
        'usuarios_id__nombre', 
        'usuarios_id__departamentosEmpresas_id__departamentos_id__nombre',
        'modelos_id__tiposEquiposMarcas_id__tiposEquipos_id__nombre',
        'empresas_id__id')
        # queryset = self.filter_queryset(self.get_queryset())
        search = self.request.query_params.get('search', None)
        # print(search)
        if search:
            queryset=queryset.filter(
            Q(serial__startswith = search) |
            Q(empresas_id__nombre__startswith = search) |
            Q(id__ubicaciones__nombre__startswith = search) |
            Q(csb__startswith = search) |
            Q(usuario_so__startswith = search) |
            Q(modelos_id__nombre__startswith = search) |
            Q(modelos_id__tiposEquiposMarcas_id__marcas_id__nombre__startswith = search) |
            Q(usuarios_id__nombre__startswith = search) 
            ) 

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = equiposSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = equiposSerializers(queryset, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     # print(kwargs['pk'])
    #     queryset = equipos.objects.filter(**kwargs)
    #     serializer = equiposSerializers(queryset, many=True)
    #     return Response(serializer.data)

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
    filterset_fields = ['id','nombre','tiposEquiposMarcas_id__tiposEquipos_id', 'tiposEquiposMarcas_id__marcas_id']
    

class marcasViewSet(viewsets.ModelViewSet):
    queryset = marcas.objects.all()
    permission_classes = [permissions.AllowAny] 
    serializer_class = marcasSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = []
    filterset_fields = ['tiposEquiposMarcas']

class informacionViewSet(viewsets.ModelViewSet):
    queryset = informacion.objects.all()
    permission_classes = [permissions.AllowAny] 
    serializer_class = informacionSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['asignacion']

class ubicacionesViewSet(viewsets.ModelViewSet):
    queryset = ubicaciones.objects.using('it_db')
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

# class departamentosViewSet(viewsets.ModelViewSet):
#     queryset = departamentos.objects.all()
#     permission_classes = [permissions.AllowAny] 
#     serializer_class = departamentosSerializers