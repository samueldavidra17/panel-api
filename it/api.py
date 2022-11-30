from .models import empresas, marcas, tipos_equipos, tipos_equipos_marcas, departamentos, ubicaciones, usuarios, informacion, modelos, equipos, impresoras, dispositivos
from rest_framework import viewsets, permissions, filters, status, mixins, generics
from .serializers import tipos_equiposSerializers, tipos_equipos_marcasSerializers, equiposSerializers, impresorasSerializers, dispositivosSerializers, modelosSerializers, marcasSerializers, informacionSerializers, ubicacionesSerializers, usuariosSerializers, departamentoSerializers, empresasSerializers, historialSerializers, UserSerializer, RegisterSerializer
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
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAuthenticatedOrReadOnly
from django.db.models import Subquery
from knox.models import AuthToken  
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

# Register API
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

class LoginAPI(KnoxLoginView):
    authentication_classes = [BasicAuthentication]
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        loggin = super(LoginAPI, self).post(request, format=None)
        # print(loggin.data)
        return loggin

class IsUser(BasePermission):
   def has_permission(self, request, view, read_only=True):
      return request.user
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class TextComboxApi(ObjectMultipleModelAPIViewSet):
    permission_classes = [permissions.AllowAny]
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
    permission_classes = [permissions.AllowAny]
    serializer_class = asignacionesSerializers

class tiposRamViewSet(viewsets.ModelViewSet):
    queryset = tiposRam.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = tiposRamSerializers

class estatusViewSet(viewsets.ModelViewSet):
    queryset = estatus.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = estatusSerializers

class soViewSet(viewsets.ModelViewSet):
    queryset = so.objects.all()
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

class historialEquiposViewSet(viewsets.ModelViewSet):
    queryset = equipos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = historialSerializers

class equiposViewSet(viewsets.ModelViewSet, GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = equiposSerializers
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['serial','serial_cargador','serial_unidad','dd','ram','tipo_ram','csb','antivirus','usuario_so','so']
    filterset_fields = ['usuarios_id']

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

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    def list(self, request):
        # print(self.get_queryset.__dict__)
        queryset = equipos.objects.values('id','empresas_id__nombre','id__ubicaciones__nombre',
        'serial','csb','usuario_so','modelos_id__nombre',
        'modelos_id__tiposEquiposMarcas_id__marcas_id__nombre', 'usuarios_id',
        'usuarios_id__nombre', 
        'usuarios_id__departamentosEmpresas_id__departamentos_id__nombre',
        'modelos_id__tiposEquiposMarcas_id__tiposEquipos_id__nombre',
        'empresas_id__id')
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
    permission_classes = [permissions.IsAuthenticated | IsUser]
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
