from rest_framework import serializers
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
#DOCUMENTACION
# model hace referencia a los modelos que vienen de py
# fields hace referencia a los campos que se encuentran o dentro del modelo o que se
# definen fuera de la clase Meta
# create crea un objeto a partir de otro
# to_representation muestra los datos que uno quiere mostrar o devolver en la vista en formato JSON
# Update actualiza los datos

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',  'first_name', 'last_name')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class EmpresasSerializers(serializers.ModelSerializer):
    empresasDepartamentos = serializers.PrimaryKeyRelatedField(queryset=Departamentos.objects.all(), many=True)

    class Meta:
        model = Empresas
        fields = ('id','nombre', 'empresasDepartamentos')
    
class DepartamentoSerializers(serializers.ModelSerializer):
    empresas = serializers.PrimaryKeyRelatedField(queryset=Empresas.objects.all(), many=True)

    class Meta:
        model = Departamentos
        fields = ('id','nombre', 'empresas')

class UsuarioSerializers(serializers.ModelSerializer):
    #se dan estos dos datos para luego que se cree la relacion si ese objeto existe
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresas.objects.all(), many=False)
    departamento = serializers.PrimaryKeyRelatedField(queryset=Departamentos.objects.all(), many=False)

    class Meta:
        model = Usuarios
        fields = ('id','cargo','nombre', 'departamento', 'empresa')
    #Se manda empresa y departamento y si ya estan relacionado ambas se trae el dato de departamentoEmpresas
    def create(self, validated_data):
        departamento = validated_data['departamento']
        empresa = validated_data['empresa']
        try:
            departamentoEmpresa = DepartamentosEmpresas.objects.get(departamentos=departamento, empresas=empresa)
            usuario = {
                'cargo': validated_data['cargo'],
                'nombre': validated_data['nombre'],
                'departamentosEmpresas': departamentoEmpresa
            }
            return Usuarios.objects.create(**usuario)
            
        except DepartamentosEmpresas.DoesNotExist:
            return HttpResponse("error message", status_code=500)

    def update(self, instance, validated_data):
        instance.nombre = validated_data['nombre']
        instance.cargo = validated_data['cargo']
        departamento = validated_data['departamento']
        empresa = validated_data['empresa']
        instance.departamentosEmpresas = DepartamentosEmpresas.objects.get(departamentos=departamento, empresas=empresa)
        instance.save()
        return instance

    def to_representation(self, value):
        return {
            "id": value.id,
            "cargo": value.cargo,
            "nombre": value.nombre,
            "departamentoNombre": value.departamentosEmpresas.departamentos.nombre,
            "departamento": value.departamentosEmpresas.departamentos.id,
            "empresa": value.departamentosEmpresas.empresas.id,
            "empresaNombre": value.departamentosEmpresas.empresas.nombre
        }

class TiposEquipoSerializers(serializers.ModelSerializer):
    class Meta:
        model = TiposEquipos
        fields = ('id','nombre')

    def create(self, validated_data):
        idEquipo = TiposEquipos.objects.filter(id__startswith=validated_data["id"]).order_by("-id").values("id")[:1]
        idNumber = idEquipo[0]["id"] if len(idEquipo) > 0 else validated_data["id"]+"-0"
        idSplit = idNumber.split("-")[1] 
        idNew = validated_data["id"]+"-"+str(int(idSplit)+1)
        tipoEquipoNew = TiposEquipos.objects.create(id=idNew, nombre=validated_data["nombre"])
        return tipoEquipoNew
       
class MarcaSerializers(serializers.ModelSerializer):
    tipoEquipos = serializers.PrimaryKeyRelatedField(queryset=TiposEquipos.objects.all(), many=False)
    modelos = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Marcas
        fields = ('id','nombre','tipoEquipos', 'modelos')

    def create(self, validated_data):
        marca = Marcas.objects.create(nombre=validated_data['nombre'])
        tiposEquiposMarcas = TiposEquiposMarcas.objects.create(marcas=marca, tiposEquipos=validated_data['tipoEquipos'])
        if(len(validated_data['modelos']) > 0):
            for x in validated_data['modelos']:
                Modelos.objects.create(nombre=x, tiposEquiposMarcas=tiposEquiposMarcas)
        return marca

    def update(self, instance, validated_data):
        instance.nombre = validated_data['nombre']
        if(len(validated_data['modelos']) > 0):
            tiposEquiposMarcas = TiposEquiposMarcas.objects.get(tiposEquipos=validated_data['tipoEquipos'], marcas=instance.id)
            for x in validated_data['modelos']:
                Modelos.objects.create(nombre=x, tiposEquiposMarcas=tiposEquiposMarcas)

        instance.save()
        return instance

    def to_representation(self, value):
        return {
            "id": value.id, 
            "nombre": value.nombre
        }


class ModeloSerializers(serializers.ModelSerializer):
    tiposEquiposMarcas = serializers.PrimaryKeyRelatedField(queryset=TiposEquiposMarcas.objects.all(), many=False)

    class Meta:
        model = Modelos
        fields = ('id','nombre','tiposEquiposMarcas')

    def to_representation(self, value):
        return {
            "id": value.id, 
            "nombre": value.nombre, 
            "tiposEquiposMarcas": value.tiposEquiposMarcas.id
        }

class UbicacioneSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ubicaciones
        fields = ('id','nombre')

class AsignacioneSerializers(serializers.ModelSerializer):
    class Meta:
        model = Asignaciones
        fields = ('id','nombre')

class EstatuSerializers(serializers.ModelSerializer):
    class Meta:
        model = Estatus
        fields = ('id','nombre')

class EstadoSerializers(serializers.ModelSerializer):
    asignacion = serializers.PrimaryKeyRelatedField(queryset=Asignaciones.objects.all(), many=False)
    estatus = serializers.PrimaryKeyRelatedField(queryset=Estatus.objects.all(), many=False)
    ubicaciones = serializers.PrimaryKeyRelatedField(queryset=Ubicaciones.objects.all(), many=False)

    class Meta:
        model = Estado
        fields = ('id','estatus','asignacion','observacion','ubicaciones')

    def to_representation(self, value):
        return {
            "id": value.id,
            "estatus": value.estatu.id,
            "asignacion": value.asignacion.id,
            "observacion": value.observacion,
            "ubicaciones": value.ubicaciones.id
        }
        
class TiposRamSerializers(serializers.ModelSerializer):
    class Meta:
        model = TiposRam
        fields = ('id','nombre')

    
class SoSerializers(serializers.ModelSerializer):
    class Meta:
        model = So
        fields = ('id','nombre')

class EquipoSerializers(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()
    so = serializers.PrimaryKeyRelatedField(queryset=So.objects.all(), many=False)
    tipo_ram = serializers.PrimaryKeyRelatedField(queryset=TiposRam.objects.all(), many=False)

    class Meta:
        model = Equipos
        fields = '__all__'
        read_only_fields = ('history',)

    def create(self, validated_data):
        info = Estado.objects.create()
        return Equipos.objects.create(id=info, **validated_data)

    def to_representation(self, value):
        #Se fragmenta para que en una vista detallada se muestren todos los datos de equipo
        if(type(value) == type({})):
            #renombro los campos user y model 
            value["usuario"] = value.pop("user")
            value["modelo"] = value.pop("model")
            return value

        usuario = ''
        departamento = ''
        cargo = ''
        #Operador ternario
        if(value.usuario is not None):
            usuario = value.usuario.nombre
            cargo = value.usuario.cargo
            departamento = value.usuario.departamentosEmpresas.departamentos.nombre
        else:
            usuario = 'S/N'
            cargo = 'S/N'
            departamento = 'S/N'
        # return value.id.estatus
        return {
            'informacion': {
                'estatus': value.id.estatu.nombre,
                'asignacion': value.id.asignacion.nombre,
                'observacion': value.id.observacion,
                'ubicacion': value.id.ubicaciones.nombre,
            },
            'id': value.id_id,
            'departamento': departamento,
            'ubicacion': value.id.ubicaciones.nombre,
            'serial': value.serial,
            'serial_cargador': value.serial_cargador,
            'serial_unidad': value.serial_unidad,
            'dd': value.dd,
            'ram': value.ram,
            'tipo_ram_nombre': value.tipo_ram.nombre,
            'tipo_ram': value.tipo_ram.id,
            'csb': value.csb,
            'tipo_equipo': value.modelo.tiposEquiposMarcas.tiposEquipos.nombre,
            'tipoEquipos_id': value.modelo.tiposEquiposMarcas.tiposEquipos.id,
            'antivirus': value.antivirus,
            'nombre': value.nombre,
            'so': value.so.id,
            'so_nombre': value.so.nombre,
            'modelo': value.modelo.nombre,
            'modelo_id': value.modelo.id,
            'marca': value.modelo.tiposEquiposMarcas.marcas.nombre,
            'marca_id': value.modelo.tiposEquiposMarcas.marcas.id,
            'usuario': usuario,
            'usuario_cargo': cargo,
            'empresa_id': value.empresas.id
        }

class HistoricalRecordField(serializers.ModelSerializer):
    #Creando el historial o la bitacora con la libreria de django-simple-history
    def __init__(self, model, *args, fields='__all__', **kwargs):
        self.Meta.model = model
        self.Meta.fields = fields
        super().__init__()

    class Meta:
        pass

class HistorialSerializers(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()

    class Meta:
        model = Equipos
        fields = ('history','usuario')

    def to_representation(self, value):
        #Objeto que viene desde historicalrecordfield
        model = value.history.__dict__['model']
        fields = ['usuario_id','history_date']#using('it_db')
        serializer = HistoricalRecordField(model, value.history.all(), fields=fields, many=True)
        serializer.is_valid()
        #Se define una variable para luego devolverla en un bucle que va a recorrer todos los objetos del historial
        def represetancion(x):
            return {
                "usuario": x.usuario.nombre if x.usuario is not None else "S/N",
                "cargo": x.usuario.cargo if x.usuario is not None else "S/N",
                "fecha": x.history_date if x.history_date is not None else "S/N",
                "departamento": x.usuario.departamentosEmpresas.departamentos.nombre if x.usuario is not None else "S/N",
                "observacion": x.id.observacion
            }
        historial = map(represetancion, serializer.initial_data)

        return {
            "historial": historial
        }

class ImpresoraSerializers(serializers.ModelSerializer):
    class Meta:
        model = Impresoras
        fields = ('serial','csb','tipo_conexion','ip','departamento','toner','modelos')

    def create(self, validated_data):
        info = Estado.objects.create()
        return Impresoras.objects.create(id=info, **validated_data)
    
    def to_representation(self, instance):
        return {
            "id": instance.id.id,
            "tipo_impresora": instance.modelos.tiposEquiposMarcas.tiposEquipos.nombre,
            "serial": instance.serial,
            "csb": instance.csb,
            "departamento": instance.departamento.nombre,
            "departamento_id": instance.departamento.id,
            "tipo_conexion": instance.tipo_conexion,
            "ip": instance.ip,
            "modelo": instance.modelos.nombre,
            "modelo_id": instance.modelos.id,
            "marca": instance.modelos.tiposEquiposMarcas.marcas.nombre,
            "marca_id": instance.modelos.tiposEquiposMarcas.marcas.id,
            "ubicacion": instance.id.ubicaciones.nombre,
            "estatus": instance.id.estatus,
            "toner": instance.toner,
        } 

class DispositivoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dispositivos
        fields = ('serial','csb', 'modelos','asignado')

    def create(self, validated_data):
        info = Estado.objects.create()
        return Dispositivos.objects.create(id=info, **validated_data)

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "tipo_dispositivo": instance.modelos.tiposEquiposMarcas.tiposEquipos.nombre,
            "marca": instance.modelos.tiposEquiposMarcas.marcas.nombre,
            "modelo": instance.modelos.nombre,
            "serial": instance.serial,
            "tipo_dispositivo_id": instance.modelos.tiposEquiposMarcas.tiposEquipos.id,
            "modelo_id": instance.modelos.id,
            "marca_id": instance.modelos.tiposEquiposMarcas.marcas.id,
            "usuario": instance.asignado.usuario_so if instance.asignado is not None else "Sin asignar",
            "departamento": instance.asignado.usuarios.departamentosEmpresas.departamentos.nombre 
                            if instance.asignado is not None and instance.asignado.usuarios is not None
                            else "Sin asignar"
        }

class PowerBISerializers(serializers.ModelSerializer):
    class Meta:
        model = Equipos
        fields = '__all__'

    def to_representation(self, value):
        return {
            "estatus": value.id.estatu.nombre,
            "asignacion": value.id.asignacion.nombre,
            "ubicacion": value.id.ubicaciones.nombre,
            "obsercacion": value.id.observacion,
            'id': value.id_id,
            'serial': value.serial,
            'serial_cargador': value.serial_cargador,
            'serial_unidad': value.serial_unidad,
            'dd': value.dd,
            'ram': value.ram,
            'tipo_ram': value.tipo_ram.nombre,
            'csb': value.csb,
            'tipo_equipo': value.modelo.tiposEquiposMarcas.tiposEquipos.nombre,
            'antivirus': value.antivirus,
            'nombre': value.nombre,
            'so': value.so.nombre,
            'modelo': value.modelo.nombre,
            'marca': value.modelo.tiposEquiposMarcas.marcas.nombre,
            'usuario': value.usuario.nombre if value.usuario is not None else "DISPONIBLE",
            'empresa': value.empresas.nombre
        }