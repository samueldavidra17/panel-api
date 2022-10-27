from asyncio.windows_events import NULL
from contextlib import nullcontext
from pickle import FALSE
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import empresas, marcas, tipos_equipos, tipos_equipos_marcas, departamentos, ubicaciones, usuarios, informacion, modelos, equipos, impresoras, dispositivos


class impresorasSerializers(serializers.ModelSerializer):
    class Meta:
        model = impresoras
        fields = ('id','codigo_inventario','serial','csb','cbc','tipo_impresion','tipo_conexion','ip','propiedad','informacionforeignkey','modelosforeignkey')

class dispositivosSerializers(serializers.ModelSerializer):
    class Meta:
        model = dispositivos
        fields = ('id','serial','informacionforeignkey','modelosforeignkey','usuariosforeignkey')

class modelosSerializers(serializers.ModelSerializer):
    class Meta:
        model = modelos
        fields = ('id','nombre','tipos_equipos_marcas')

    def to_representation(self, value):
        return {"id": value.id, "nombre": value.nombre, "marca": value.tipos_equipos_marcas.marcasforeignkey.nombre}

class marcasSerializers(serializers.ModelSerializer):
    class Meta:
        model = marcas
        fields = ('id','nombre')

class informacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = informacion
        fields = ('id','estatus','asignacion','observacion','ubicacionesforeignkey')

    def to_representation(self, value):
        return {"id": value.id, "estatus": value.estatus, "asignacion": value.asignacion, "observacion": value.observacion, 
        "ubicacionesforeignkey":{"id": value.ubicacionesforeignkey.id, "nombre": value.ubicacionesforeignkey.nombre}}

class equiposSerializers(serializers.ModelSerializer):
    class Meta:
        model = equipos
        fields = ('id','tipo_equipo','serial','serial_cargador','serial_unidad','dd','ram','tipo_ram','csb','tipo_equipo','antivirus','usuario_so','so','modelosforeignkey','usuariosforeignkey','empresasforeignkey')
        validators = [
            UniqueTogetherValidator(
                queryset=equipos.objects.all(),
                fields=['usuariosforeignkey']
            )
        ]
        usuariosforeignkey = serializers.CharField(allow_null=True,source="usuariosforeignkey",required=False)
        modelosforeignkey = serializers.CharField(allow_null=True,source="modelosforeignkey",required=False)
    def to_representation(self, value):
        usuario = ''
        usuario_id = ''
        if(value.usuariosforeignkey is not None):
            usuario = value.usuariosforeignkey.nombre
            usuario_id = value.usuariosforeignkey.id
            usuario_id_empresa = value.empresasforeignkey.id
        else:
            usuario = 'S/N'
            usuario_id = ''
            usuario_id_empresa = ''
        # print(value.modelosforeignkey is not None if value.modelosforeignkey.nombre else 'nada')
        return {
            'informacion': {
                'estatus': value.id.estatus,
                'asignacion': value.id.asignacion,
                'observacion': value.id.observacion,
                'ubicacion': value.id.ubicacionesforeignkey.nombre,
            },
            'id': value.id_id,
            'serial': value.serial,
            'serial_cargador': value.serial_cargador,
            'serial_unidad': value.serial_unidad,
            'dd': value.dd,
            'ram': value.ram,
            'tipo_ram': value.tipo_ram,
            'csb': value.csb,
            'tipo_equipo': value.tipo_equipo,
            'antivirus': value.antivirus,
            'usuario_so': value.usuario_so,
            'so': value.so, 
            'modelos': value.modelosforeignkey.nombre,
            'modelo_id': value.modelosforeignkey.id,
            'marca': value.modelosforeignkey.tipos_equipos_marcas.marcasforeignkey.nombre,
            'marca_id': value.modelosforeignkey.tipos_equipos_marcas.marcasforeignkey.id,
            'usuario': usuario,
            'empresa_id': usuario_id_empresa
        }

class equiposSerializersMin(serializers.ModelSerializer):
    class Meta:
        model = equipos
        fields = ('id','serial','csb','tipo_equipo','usuario_so','modelosforeignkey','usuariosforeignkey','empresasforeignkey')
        validators = [
            UniqueTogetherValidator(
                queryset=equipos.objects.all(),
                fields=['usuariosforeignkey']
            )
        ]
        usuariosforeignkey = serializers.CharField(allow_null=True,source="usuariosforeignkey",required=False)
        modelosforeignkey = serializers.CharField(allow_null=True,source="modelosforeignkey",required=False)
    
    def to_representation(self, value):
        # print(value)
        usuario = ''
        usuario_id = ''
        usuario_id_empresa = ''
        if(value["usuariosforeignkey_id__nombre"] is not None):
            usuario = value["usuariosforeignkey_id__nombre"]
            usuario_id = value["usuariosforeignkey_id"]
            usuario_id_empresa = value["empresasforeignkey_id__id"]
        else:
            usuario = 'Disponible'
            usuario_id = ''
            usuario_id_empresa = ''
        # print(value.modelosforeignkey is not None if value.modelosforeignkey.nombre else 'nada')
        return {
            "id": value["id"], 
            "serial": value["serial"], 
            "csb": value["csb"], 
            "tipo_equipo": value["tipo_equipo"], 
            "usuario_so": value["usuario_so"], 
            "modelo": value["modelosforeignkey_id__nombre"], 
            "marca": value["modelosforeignkey_id__tipos_equipos_marcas_id__marcasforeignkey_id__nombre"], 
            "usuario": usuario, 
            "empresa_id": usuario_id_empresa
        }

class ubicacionesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ubicaciones
        fields = ('id','nombre')


class usuariosSerializers(serializers.ModelSerializer):
    class Meta: 
        model = usuarios
        fields = ('id','cargo','nombre','departamentosforeignkey','empresasforeignkey','equipos_us')
    def to_representation(self, value):
        # if(equipos.value.usuariosforeignkey):
        equipos_us=equiposSerializers(many=True,required=False).data
        return {"id": value.id, "cargo": value.cargo, "nombre": value.nombre, "departamento": {"nombre": value.departamentosforeignkey.nombre, "empresa": {"id": value.empresasforeignkey.id}},"equipos": equipos_us}

class empresasSerializers(serializers.ModelSerializer):
    empresas_us = serializers.PrimaryKeyRelatedField(queryset=departamentos.objects.all(), many=True)
    class Meta:
        model = empresas
        fields = ('id','nombre', 'empresas_us')

class departamentoSerializers(serializers.ModelSerializer):
    empresas = serializers.PrimaryKeyRelatedField(queryset=empresas.objects.all(), many=True)
    class Meta:
        model = departamentos
        fields = ('id','nombre', 'empresas')
    # def to_representation(self, value):
    #     return {"id": value.id, "nombre": value.nombre}

class tipos_equiposSerializers(serializers.ModelSerializer):
    class Meta:
        model = tipos_equipos
        fields = ('id','nombre')

class tipos_equipos_marcasSerializers(serializers.ModelSerializer):
    class Meta:
        model = tipos_equipos_marcas
        fields = ('id','marcasforeignkey','tipos_equiposforeignkey')
# class departamentosSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = departamentos
#         fields = ('id','nombre','departamentos_de')
    
#     departamentos_de = departamento_empresasSerializers(many=True, required=False)

