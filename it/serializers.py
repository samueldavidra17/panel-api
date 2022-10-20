from asyncio.windows_events import NULL
from contextlib import nullcontext
from pickle import FALSE
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import empresas, marcas, departamentos, ubicaciones, usuarios, informacion, modelos, equipos, impresoras, dispositivos


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
        fields = ('id','nombre','marcasforeignkey')

    def to_representation(self, value):
        return {"id": value.id, "nombre": value.nombre, "marca": value.marcasforeignkey.nombre}

class marcasSerializers(serializers.ModelSerializer):
    class Meta:
        model = marcas
        fields = ('id','nombre')

class informacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = informacion
        fields = ('id','estatus','asignacion','observacion','ubicacionesforeignkey')

    def to_representation(self, value):
        return {"id": value.id, "estatus": value.estatus, "asignacion": value.asignacion, "observacion": value.observacion, "ubicacion": value.ubicacionesforeignkey.nombre}

class equiposSerializers(serializers.ModelSerializer):
    class Meta:
        model = equipos
        fields = ('id','serial','serial_cargador','serial_unidad','dd','ram','tipo_ram','csb','tipo_equipo','antivirus','usuario_so','so','modelosforeignkey','usuariosforeignkey')
        validators = [
            UniqueTogetherValidator(
                queryset=equipos.objects.all(),
                fields=['usuariosforeignkey']
            )
        ]
    def to_representation(self, value):
            return {'id': value.id_id,'serial': value.serial,'serial_cargador': value.serial_cargador,'serial_unidad': value.serial_unidad,'dd': value.dd,'ram': value.ram,'tipo_ram': value.tipo_ram,'csb': value.csb,'tipo_equipo': value.tipo_equipo,'antivirus': value.antivirus,'usuario_so': value.usuario_so,'so': value.so,'modelo': value.modelosforeignkey.nombre ,'usuario': { 'id': value.usuariosforeignkey.id, 'nombre': value.usuariosforeignkey.nombre}}

class ubicacionesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ubicaciones
        fields = ('id','nombre','empresasforeingkey')


class usuariosSerializers(serializers.ModelSerializer):
    class Meta: 
        model = usuarios
        fields = ('id','cargo','nombre','departamentosforeignkey','equipos_us')
    def to_representation(self, value):
        # if(equipos.value.usuariosforeignkey):
        equipos_us=equiposSerializers(many=True,required=False).data
        return {"id": value.id, "cargo": value.cargo, "nombre": value.nombre, "departamento": {"nombre": value.departamentosforeignkey.nombre, "empresa": {"id": value.departamentosforeignkey.empresasforeignkey.id, "nombre": value.departamentosforeignkey.empresasforeignkey.nombre}},"equipos": equipos_us}


class departamentoSerializers(serializers.ModelSerializer):
    class Meta:
        model = departamentos
        fields = ('id','nombre','empresasforeignkey')

    def to_representation(self, value):
        return {"id": value.id, "nombre": value.nombre, "empresa": value.empresasforeignkey.nombre}

class empresasSerializers(serializers.ModelSerializer):
    class Meta:
        model = empresas
        fields = ('id','nombre')
    

# class departamentosSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = departamentos
#         fields = ('id','nombre','departamentos_de')
    
#     departamentos_de = departamento_empresasSerializers(many=True, required=False)

