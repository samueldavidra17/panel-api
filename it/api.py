from .models import empresas, marcas, departamentos, ubicaciones, usuarios, informacion, modelos, equipos, impresoras, dispositivos
from rest_framework import viewsets, permissions, filters
from .serializers import equiposSerializers, equiposSerializersMin, impresorasSerializers, dispositivosSerializers, modelosSerializers, marcasSerializers, informacionSerializers, ubicacionesSerializers, usuariosSerializers, departamentoSerializers, empresasSerializers
import django_filters.rest_framework 

class equiposViewSet(viewsets.ModelViewSet):
    queryset = equipos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = equiposSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['serial','serial_cargador','serial_unidad','dd','ram','tipo_ram','csb','tipo_equipo','antivirus','usuario_so','so']
    filterset_fields = ['usuariosforeignkey_id']
    # http_method_names = ['patch','get']

class equiposViewSetMin(viewsets.ModelViewSet):
    queryset = equipos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = equiposSerializersMin
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['serial','serial_cargador','serial_unidad','csb','tipo_equipo','antivirus','usuario_so']
    filterset_fields = ['usuariosforeignkey_id']
    # http_method_names = ['patch','get']

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
    filterset_fields = ['id','nombre','marcasforeignkey_id']
    

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
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['empresasforeingkey_id']

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