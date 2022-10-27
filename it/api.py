from .models import empresas, marcas, tipos_equipos, tipos_equipos_marcas, departamentos, ubicaciones, usuarios, informacion, modelos, equipos, impresoras, dispositivos
from rest_framework import viewsets, permissions, filters
from .serializers import tipos_equiposSerializers, tipos_equipos_marcasSerializers, equiposSerializers, equiposSerializersMin, impresorasSerializers, dispositivosSerializers, modelosSerializers, marcasSerializers, informacionSerializers, ubicacionesSerializers, usuariosSerializers, departamentoSerializers, empresasSerializers
import django_filters.rest_framework 
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

class tipos_equiposViewSet(viewsets.ModelViewSet):
    queryset = tipos_equipos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = tipos_equiposSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['nombre']

class tipos_equipos_marcasViewSet(viewsets.ModelViewSet):
    queryset = tipos_equipos_marcas.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = tipos_equipos_marcasSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['marcasforeignkey_id__nombre','tipos_equiposforeignkey_id__nombre']

class equiposViewSet(viewsets.ModelViewSet):
    queryset = equipos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = equiposSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['serial','serial_cargador','serial_unidad','dd','ram','tipo_ram','csb','tipo_equipo','antivirus','usuario_so','so']
    filterset_fields = ['usuariosforeignkey_id']
    # http_method_names = ['patch','get']

class equiposViewSetMin(viewsets.ModelViewSet):
    queryset = equipos.objects.all().values('id',
    'serial','csb','tipo_equipo','usuario_so','modelosforeignkey_id__nombre',
    'modelosforeignkey_id__tipos_equipos_marcas_id__marcasforeignkey_id__nombre', 'usuariosforeignkey_id',
    'usuariosforeignkey_id__nombre', 
    'empresasforeignkey_id__id')
    permission_classes = [permissions.AllowAny]
    serializer_class = equiposSerializersMin
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['serial','csb','usuario_so','usuariosforeignkey_id__nombre']
    filterset_fields = ['usuariosforeignkey_id']
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
    filterset_fields = ['id','nombre','tipos_equipos_marcas_id']
    

class marcasViewSet(viewsets.ModelViewSet):
    queryset = marcas.objects.all()
    permission_classes = [permissions.AllowAny] 
    serializer_class = marcasSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = []

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
    filter_backends = [filters.SearchFilter]
    search_fields = []

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