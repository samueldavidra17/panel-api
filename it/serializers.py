from asyncio.windows_events import NULL
from contextlib import nullcontext
from pickle import FALSE
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import departamentos_empresas, empresas, marcas, tipos_equipos, tipos_equipos_marcas, departamentos, ubicaciones, usuarios, informacion, modelos, equipos, impresoras, dispositivos
from django.http import HttpResponse
from jSon.models import asignaciones, estatus, tiposRam, so
from django.contrib.auth.models import User
# from .json import

# def my_custom_error_view(request):
#     return HttpResponse("error message", status_code=404)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class impresorasSerializers(serializers.ModelSerializer):
    class Meta:
        model = impresoras
        fields = ('tipo_impresion','serial','csb','tipo_conexion','ip','departamento','toner','modelos')

        def create(self, validated_data):
            info = informacion.objects.create()
            return impresoras.objects.create(id=info, **validated_data)

class dispositivosSerializers(serializers.ModelSerializer):
    class Meta:
        model = dispositivos
        fields = ('id','serial','informacion','modelos','usuarios')

class tipos_equiposSerializers(serializers.ModelSerializer):
    # marcas = serializers.PrimaryKeyRelatedField(queryset=marcas.objects.all(), many=True)
    class Meta:
        model = tipos_equipos
        fields = ('id','nombre')

class tipos_equipos_marcasSerializers(serializers.ModelSerializer):
    class Meta:
        model = tipos_equipos_marcas
        fields = ('id','marcas')

class marcasSerializers(serializers.ModelSerializer):
    tipoEquipos = serializers.PrimaryKeyRelatedField(queryset=tipos_equipos.objects.all(), many=False)
    modelos = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = marcas
        fields = ('id','nombre','tipoEquipos', 'modelos')

    def create(self, validated_data):
        marca = marcas.objects.create(nombre=validated_data['nombre'])
        tiposEquiposMarcas = tipos_equipos_marcas.objects.create(marcas=marca, tiposEquipos=validated_data['tipoEquipos'])
        if(len(validated_data['modelos']) > 0):
            for x in validated_data['modelos']:
                modelos.objects.create(nombre=x, tiposEquiposMarcas=tiposEquiposMarcas)
        return marca

    def update(self, instance, validated_data):
        instance.nombre = validated_data['nombre']
        if(len(validated_data['modelos']) > 0):
            tiposEquiposMarcas = tipos_equipos_marcas.objects.get(tiposEquipos=validated_data['tipoEquipos'], marcas=instance.id)
            for x in validated_data['modelos']:
                modelos.objects.create(nombre=x, tiposEquiposMarcas=tiposEquiposMarcas)

        instance.save()
        return instance

    def to_representation(self, value):
        return {"id": value.id, "nombre": value.nombre}


class modelosSerializers(serializers.ModelSerializer):
    tiposEquiposMarcas = serializers.PrimaryKeyRelatedField(queryset=tipos_equipos_marcas.objects.all(), many=False)

    class Meta:
        model = modelos
        fields = ('id','nombre','tiposEquiposMarcas')

    def to_representation(self, value):
        return {"id": value.id, "nombre": value.nombre, "tiposEquiposMarcas": value.tiposEquiposMarcas.id}

class informacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = informacion
        fields = ('id','estatus','asignacion','observacion','ubicaciones')

    def to_representation(self, value):
        return {
            "id": value.id,
            "estatus": value.estatus,
            "asignacion": value.asignacion,
            "observacion": value.observacion,
            "ubicaciones":{
                "id": value.ubicaciones.id,
                "nombre": value.ubicaciones.nombre
            }
        }

class HistoricalRecordField(serializers.ModelSerializer):#.ListField):
    #FASE 2 DE EXPERIMENTACIÓN CON LAS HISTORIAS##
    def __init__(self, model, *args, fields='__all__', **kwargs):
        self.Meta.model = model
        self.Meta.fields = fields
        # print(fields)
        super().__init__()

    class Meta:
        pass

    ##FASE 1 DE EXPERIMENTACIÓN CON LAS HISTORIAS##
    # child = serializers.DictField()

    # def to_representation(self, data):
    #     return super().to_representation(data.values())


class historialSerializers(serializers.ModelSerializer):
    class Meta:
        model = equipos
        fields = ('history','usuarios')

    history = serializers.SerializerMethodField()

    def to_representation(self, value):
        model = value.history.__dict__['model']
        fields = ['usuarios_id','history_date']#using('it_db')
        serializer = HistoricalRecordField(model, value.history.all(), fields=fields, many=True)
        serializer.is_valid()
        def represetancion(x):
            return {
                "usuario": x.usuarios.nombre if x.usuarios is not None else "S/N",
                "cargo": x.usuarios.cargo if x.usuarios is not None else "S/N",
                "fecha": x.history_date if x.history_date is not None else "S/N",
                "departamento": x.usuarios.departamentosEmpresas.departamentos.nombre if x.usuarios is not None else "S/N",
                "observacion": x.id.observacion
            }
        historial = map(represetancion, serializer.initial_data)

        return{
            "historial": historial
        }
class equiposSerializers(serializers.ModelSerializer):
    # history = HistoricalRecordField(read_only=True)
    class Meta:
        model = equipos
        fields = ('serial','serial_cargador','serial_unidad','dd','ram','tipo_ram','csb','antivirus','usuario_so','so','modelos','usuarios','empresas', 'history')
        extra_kwargs = {'serial':{"default": ''}}
        read_only_fields = ('history',)
        # query = equipos.objects.all().values('id__asignacion')
        # for i in query:
        #     valor = i['id__asignacion']
        #     if(valor == "PRESTAMO"):
        #     else:
        #         print('hola')
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=equipos.objects.all(),
        #         fields=['usuarios']
        #     )
        # ]

        usuarios = serializers.CharField(allow_null=True,source="usuarios",required=False)
        modelos = serializers.CharField(allow_null=True,source="modelos",required=False)
    history = serializers.SerializerMethodField()

    # def get_history(self, obj):
    #     # using slicing to exclude current field values
    #     h = obj.history.all()
    #     return h

    def validate(self, value):
        qs = equipos.objects.filter(usuarios=value["usuarios"])
        if(self.__dict__['_args'] == ()):
            asignar = "Por Asignar"
        else:
            asignar = self.__dict__['_args'][0].id.asignacion
        # filt = equipos.objects.filter(id=intoSelf)
        # asignar = filt[0].id.asignacion
        if(asignar != "PRESTAMO"):
            if(value["usuarios"] != None):
                if qs.exists():
                    raise serializers.ValidationError('Name must be unique per site')
        return value

    # def validate(self, value):
    #     # qs = equipos.objects.filter(self._meta.unique_together)
    #     # print(qs)
    #     if(value["id"].asignacion != "PRESTAMO"):
    #         print(value["usuarios"].nombre if value["usuarios"] is not None else "S/N")
    #         print(value["usuarios"].id if value["usuarios"] is not None else "S/N")
    #         if(value["usuarios"].id != 1 if value["usuarios"] is not None else "S/N"):
    #             raise serializers.ValidationError("ERROR")
    #     return value

    def create(self, validated_data):
        info = informacion.objects.create()
        return equipos.objects.create(id=info, **validated_data)

    # def update(self, instance, validated_data):
    #     instance.serial = validated_data['serial']
    #     instance.tipos_equipo = validated_data['tipos_equipo']
    #     instance.serial_cargador = validated_data['serial_cargador']
    #     instance.serial_unidad = validated_data['serial_unidad']
    #     instance.cargo = validated_data['cargo']
    #     instance.departamentosEmpresas = departamentos_empresas.objects.get(departamentos=validated_data['departamento'], empresas=validated_data['empresa'])
    #     instance.save()
    #     return instance

    def to_representation(self, value):
        # if(value.id.asignacion == 'PRESTAMO'):
        #     print('hola')
        if(type(value) != type({})):
            model = value.history.__dict__['model']
            # print(value.id.observacion)
            fields = ['usuarios_id']#using('it_db')
            serializer = HistoricalRecordField(model, value.history.all(), fields=fields, many=True)
            serializer.is_valid()
            def represetancion(x):
                return {
                    "nombre": x.usuarios.nombre if x.usuarios is not None else "S/N",
                    "depatamento": x.usuarios.departamentosEmpresas.departamentos.nombre if x.usuarios is not None else "S/N",
                    "observacion": x.id.observacion
                }
            historial = map(represetancion, serializer.initial_data)
            usuario = ''
            usuario_id = ''
            departamento = ''
            if(value.usuarios is not None):
                usuario = value.usuarios.nombre
                usuario_id = value.usuarios.id
                usuario_id_empresa = value.empresas.id if value.empresas is not None else "S/N"
                departamento = value.usuarios.departamentosEmpresas.departamentos.nombre
            else:
                usuario = 'S/N'
                usuario_id = ''
                usuario_id_empresa = ''
                departamento = 'It'
            # return value.id.estatus
            return {
                'informacion': {
                    'estatus': value.id.estatus,
                    'asignacion': value.id.asignacion,
                    'observacion': value.id.observacion,
                    'ubicacion': value.id.ubicaciones.nombre,
                },
                'id': value.id_id,
                # 'empresa': value.empresas.nombre,
                'departamento': departamento,
                'ubicacion': value.id.ubicaciones.nombre,
                'serial': value.serial,
                'serial_cargador': value.serial_cargador,
                'serial_unidad': value.serial_unidad,
                'dd': value.dd,
                'ram': value.ram,
                'tipo_ram': value.tipo_ram,
                'csb': value.csb,
                'tipo_equipo': value.modelos.tiposEquiposMarcas.tiposEquipos.nombre,
                'tipoEquipos_id': value.modelos.tiposEquiposMarcas.tiposEquipos.id,
                'antivirus': value.antivirus,
                'usuario_so': value.usuario_so,
                'so': value.so,
                'modelos': value.modelos.nombre,
                'modelo_id': value.modelos.id,
                'marca': value.modelos.tiposEquiposMarcas.marcas.nombre,
                'marca_id': value.modelos.tiposEquiposMarcas.marcas.id,
                'usuario': usuario,
                'empresa_id': value.empresas.id if value.empresas is not None else "S/N",
                'historial': historial
            }
        else:
            usuario = ''
            usuario_id = ''
            usuario_id_empresa = ''
            if(value["usuarios_id"] is not None):
                usuario = value["usuarios_id__nombre"]
                usuario_id = value["usuarios_id"]
                usuario_id_empresa = value["empresas_id__id"]
                departamento = value["usuarios_id__departamentosEmpresas_id__departamentos_id__nombre"]
            else:
                usuario = 'Disponible'
                usuario_id = ''
                usuario_id_empresa = ''
                departamento = 'It'
            return {
            "id": value["id"],
            # "empresa": value["empresas_id__nombre"],
            "ubicacion": value["id__ubicaciones__nombre"],
            "serial": value["serial"],
            "csb": value["csb"],
            "tipo_equipo": value["modelos_id__tiposEquiposMarcas_id__tiposEquipos_id__nombre"],
            "usuario_so": value["usuario_so"],
            "modelo": value["modelos_id__nombre"],
            "marca": value["modelos_id__tiposEquiposMarcas_id__marcas_id__nombre"],
            "usuario": usuario,
            "departamento": departamento,
            # "historial": self.__dict__['_args']
        }

class equiposSerializersMin(serializers.ModelSerializer):
    class Meta:
        model = equipos
        fields = ('id','serial','csb','usuario_so','modelos','usuarios','empresas')
        validators = [
            UniqueTogetherValidator(
                queryset=equipos.objects.all(),
                fields=['usuarios']
            )
        ]
        usuarios = serializers.CharField(allow_null=True,source="usuarios",required=False)
        modelos = serializers.CharField(allow_null=True,source="modelos",required=False)

    def to_representation(self, value):
        # print(value)
        usuario = ''
        usuario_id = ''
        usuario_id_empresa = ''
        if(value["usuarios_id__nombre"] is not None):
            usuario = value["usuarios_id__nombre"]
            usuario_id = value["usuarios_id"]
            usuario_id_empresa = value["empresas_id__id"]
        else:
            usuario = 'Disponible'
            usuario_id = ''
            usuario_id_empresa = ''
        # print(value.modelos is not None if value.modelos.nombre else 'nada')
        return {
            "id": value["id"],
            "empresa": value["empresas_id__nombre"],
            "ubicacion": value["id__ubicaciones__nombre"],
            "serial": value["serial"],
            "csb": value["csb"],
            # "tipo_equipo": value["tipo_equipo"],
            "usuario_so": value["usuario_so"],
            "modelo": value["modelos_id__nombre"],
            "marca": value["modelos_id__tiposEquiposMarcas_id__marcas_id__nombre"],
            "usuario": usuario,
            "empresa_id": usuario_id_empresa
        }

class ubicacionesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ubicaciones
        fields = ('id','nombre')

class empresasSerializers(serializers.ModelSerializer):
    empresasDepartamentos = serializers.PrimaryKeyRelatedField(queryset=departamentos.objects.all(), many=True)
    class Meta:
        model = empresas
        fields = ('id','nombre', 'empresasDepartamentos')

class departamentoSerializers(serializers.ModelSerializer):
    empresas = serializers.PrimaryKeyRelatedField(queryset=empresas.objects.all(), many=True)
    class Meta:
        model = departamentos
        fields = ('id','nombre', 'empresas')
    # def to_representation(self, value):
    #     return {"id": value.id, "nombre": value.nombre}

class usuariosSerializers(serializers.ModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(queryset=empresas.objects.all(), many=False)
    departamento = serializers.PrimaryKeyRelatedField(queryset=departamentos.objects.all(), many=False)
    class Meta:
        model = usuarios
        fields = ('id','cargo','nombre', 'departamento', 'empresa')

    def create(self, validated_data):
        try:
            departamentoEmpresa = departamentos_empresas.objects.get(departamentos=validated_data['departamento'], empresas=validated_data['empresa'])
            usuario = {
                'cargo': validated_data['cargo'],
                'nombre': validated_data['nombre'],
                'departamentosEmpresas': departamentoEmpresa
            }
            return usuarios.objects.create(**usuario)
        except departamentos_empresas.DoesNotExist:
            return HttpResponse("error message", status_code=500)

    def update(self, instance, validated_data):
        instance.nombre = validated_data['nombre']
        instance.cargo = validated_data['cargo']
        instance.departamentosEmpresas = departamentos_empresas.objects.get(departamentos=validated_data['departamento'], empresas=validated_data['empresa'])
        instance.save()
        return instance

    def to_representation(self, value):
        # if(equipos.value.usuarios):
        # equiposUs=equiposSerializers(many=True,required=False).data
        return {
            "id": value.id,
            "cargo": value.cargo,
            "nombre": value.nombre,
            "departamento": value.departamentosEmpresas.departamentos.nombre,
            "departamentoId": value.departamentosEmpresas.departamentos.id,
            "empresaId": value.departamentosEmpresas.empresas.id,
            "empresa": value.departamentosEmpresas.empresas.nombre
        }

# class departamentosSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = departamentos
#         fields = ('id','nombre','departamentos_de')

#     departamentos_de = departamento_empresasSerializers(many=True, required=False)

