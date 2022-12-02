from rest_framework import serializers
from .models import departamentos_empresas, empresas, marcas, tipos_equipos, tipos_equipos_marcas, departamentos, ubicaciones, usuarios, informacion, modelos, equipos, impresoras, dispositivos
from django.http import HttpResponse
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup as b


###Web Scrapy no implementado por falta de tiempo###
url = 'http://172.17.247.247/SSI/info_configuration.htm'
def get_count(url):
    req = requests.get(url)
    html = b(req.text, "html.parser")
    entradas = html.find_all('table',{'class':'mainContentArea'})
    for i, buscar in enumerate(entradas):
        busqueda = buscar.find(['tr',{'class':'itemFont'}]).getText()
        iterator = i+1
        if(iterator == 2):
            return busqueda
count1 = get_count(url).split(":")[1]

# from .json import

# def my_custom_error_view(request):
#     return HttpResponse("error message", status_code=404)


#DOCUMENTACION
# model hace referencia a los modelos que vienen de models.py
# fields hace referencia a los campos que se encuentran o dentro del modelo o que se
# definen fuera de la clase Meta
# create crea un objeto a partir de otro
# to_representation muestra los datos que uno quiere mostrar o devolver en la vista en formato JSON
# Update actualiza los datos

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
        fields = ('serial','csb','tipo_conexion','ip','departamento','toner','modelos')

    def create(self, validated_data):
        info = informacion.objects.create()
        return impresoras.objects.create(id=info, **validated_data)
    
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

class dispositivosSerializers(serializers.ModelSerializer):
    class Meta:
        model = dispositivos
        fields = ('serial','csb', 'modelos','asignado')
    
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

class tipos_equiposSerializers(serializers.ModelSerializer):
    class Meta:
        model = tipos_equipos
        fields = ('id','nombre')

    def create(self, validated_data):
        idEquipo = tipos_equipos.objects.filter(id__startswith=validated_data["id"]).order_by("-id").values("id")[:1]
        idNumber = idEquipo[0]["id"] if len(idEquipo) > 0 else validated_data["id"]+"-0"
        idSplit = idNumber.split("-")[1] 
        idNew = validated_data["id"]+"-"+str(int(idSplit)+1)
        tipoEquipoNew = tipos_equipos.objects.create(id=idNew, nombre=validated_data["nombre"])
        return tipoEquipoNew
       

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
    #Creando el historial o la bitacora con la libreria de django-simple-history
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

    def create(self, validated_data):
        print(validated_data)
        info = informacion.objects.create()
        return equipos.objects.create(id=info, **validated_data)

    def to_representation(self, value):
        #Objeto que viene desde historicalrecordfield
        model = value.history.__dict__['model']
        fields = ['usuarios_id','history_date']#using('it_db')
        serializer = HistoricalRecordField(model, value.history.all(), fields=fields, many=True)
        serializer.is_valid()
        #Se define una variable para luego devolverla en un bucle que va a recorrer todos los objetos del historial
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
    history = serializers.SerializerMethodField()
    
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


    # def get_history(self, obj):
    #     # using slicing to exclude current field values
    #     h = obj.history.all()
    #     return h

    def create(self, validated_data):
        info = informacion.objects.create()
        return equipos.objects.create(id=info,  **validated_data)
    #Validando si el equipo se encuentra en prestamo para asignarlo a más de un usuario
    #O que si no, no pueda tener más de un equipo
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
        #Se fragmenta para que en una vista detallada se muestren todos los datos de equipo
        #Y en el otro solo unos especificos
        if(type(value) != type({})):
            #Objeto que viene desde historicalrecordfield
            model = value.history.__dict__['model']
            fields = ['usuarios_id']
            serializer = HistoricalRecordField(model, value.history.all(), fields=fields, many=True)
            serializer.is_valid()
            #Se define una variable para luego devolverla en un bucle que va a recorrer todos los objetos del historial
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
            #Operador ternario
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

class usuariosSerializers(serializers.ModelSerializer):
    #se dan estos dos datos para luego que se cree la relacion si ese objeto existe
    empresa = serializers.PrimaryKeyRelatedField(queryset=empresas.objects.all(), many=False)
    departamento = serializers.PrimaryKeyRelatedField(queryset=departamentos.objects.all(), many=False)
    class Meta:
        model = usuarios
        fields = ('id','cargo','nombre', 'departamento', 'empresa')

    #Se manda empresa y departamento y si ya estan relacionado ambas se trae el dato de departamentoEmpresas
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
        return {
            "id": value.id,
            "cargo": value.cargo,
            "nombre": value.nombre,
            "departamentoNombre": value.departamentosEmpresas.departamentos.nombre,
            "departamento": value.departamentosEmpresas.departamentos.id,
            "empresa": value.departamentosEmpresas.empresas.id,
            "empresaNombre": value.departamentosEmpresas.empresas.nombre
        }