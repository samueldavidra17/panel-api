from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat

# Create your models here.

# class departamentos(models.Model):
#     nombre = models.CharField(max_length=45)

class empresas(models.Model):
    nombre = models.CharField(max_length=45)

class marcas(models.Model):
    nombre = models.CharField(max_length=45)

class tipos_equipos(models.Model):
    nombre = models.CharField(max_length=45)
    marcas = models.ManyToManyField(marcas, related_name="tiposEquiposMarcas", through="tipos_equipos_marcas")

    def Test(request):
     query = tipos_equipos.objects.annotate(C=Concat('1',Value('-') ,'2',
                 output_field=CharField()))

class tipos_equipos_marcas(models.Model):
    marcas = models.ForeignKey(marcas, on_delete=models.CASCADE, related_name="marcasId", null="True")
    tiposEquipos = models.ForeignKey(tipos_equipos, on_delete=models.CASCADE, related_name="tiposEquiposId", null="True")

class departamentos(models.Model):
    # departamentos = models.ForeignKey(departamentos, on_delete=models.CASCADE, related_name="departamentos_de", null="True")
    nombre = models.CharField(max_length=45)
    empresas = models.ManyToManyField(empresas, related_name="empresasDepartamentos", through="departamentos_empresas")

class departamentos_empresas(models.Model):
    departamentos = models.ForeignKey(departamentos, on_delete=models.CASCADE, related_name="empresasId", null=False)
    empresas = models.ForeignKey(empresas, on_delete=models.CASCADE, related_name="departamentosId", null=False)
    
class ubicaciones(models.Model):
    nombre = models.CharField(max_length=45)

class usuarios(models.Model):
    nombre = models.CharField(max_length=45)
    cargo = models.CharField(max_length=45)
    departamentosEmpresas = models.ForeignKey(departamentos_empresas, on_delete=models.CASCADE, related_name="departamentoEmpresaUs", null=False)

class informacion(models.Model):
    estatus = models.CharField(max_length=45)
    asignacion = models.CharField(max_length=45)
    observacion = models.TextField()
    ubicaciones = models.ForeignKey(ubicaciones, on_delete=models.CASCADE, related_name="ubicacionesUser", default=1)
    # usuarios = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name="informacion_us", null="True")

class modelos(models.Model):
    nombre = models.CharField(max_length=45)
    tiposEquiposMarcas = models.ForeignKey(tipos_equipos_marcas, on_delete=models.CASCADE, related_name="tiposEquiposMarcasId", null="True")

class equipos(models.Model):
    id = models.OneToOneField(informacion, primary_key=True, unique=True, on_delete=models.CASCADE, related_name="informacion_eq")
    empresas = models.ForeignKey(empresas, on_delete=models.CASCADE, related_name="empresasEq", null="True")
    tipo_equipo = models.CharField(max_length=45)
    modelos = models.ForeignKey(modelos, on_delete=models.CASCADE, related_name="modelosEq", null=False)
    serial = models.CharField(max_length=45)
    serial_unidad = models.CharField(max_length=45)
    serial_cargador = models.CharField(max_length=45)
    csb= models.CharField(max_length=45)
    dd = models.CharField(max_length=45)
    ram = models.CharField(max_length=45)
    tipo_ram = models.CharField(max_length=45)
    antivirus = models.CharField(max_length=45)
    so = models.CharField(max_length=45)
    usuario_so = models.CharField(max_length=45)
    usuarios = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name="equiposUs", null=True)

    # def __str__(self):
    #     return self.usuarios

    # def save(self, *args, **kwargs):
    #     if not self.pk and self.usuarios:
    #         self.usuarios.available
    #         self.usuarios.save()
    #     return super(equipos, self).save(*args, **kwargs)

class impresoras(models.Model):
    codigo_inventario = models.CharField(max_length=45)
    serial = models.CharField(max_length=45)
    csb = models.CharField(max_length=45)
    cbc = models.CharField(max_length=45)
    tipoImpresion = models.CharField(max_length=45)
    tipo_conexion = models.CharField(max_length=45)
    ip = models.CharField(max_length=45)
    propiedad = models.CharField(max_length=45)
    informacion = models.ForeignKey(informacion, on_delete=models.CASCADE, related_name="informacionIm", null="True")
    modelos = models.ForeignKey(modelos, on_delete=models.CASCADE, related_name="modelosImp", null="True")

class dispositivos(models.Model):
    serial = models.CharField(max_length=45)
    modelos = models.ForeignKey(modelos, on_delete=models.CASCADE, related_name="modelosDis", null="True")
    informacion = models.ForeignKey(informacion, on_delete=models.CASCADE, related_name="informacionDis", null="True")
    usuarios = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name="dispositivosUs", null="True")

# class capacidad_dispositivos(models.Model):
#     capacidad = models.IntegerField()
#     dispositivosforeignkey = models.ForeignKey(dispositivos, on_delete=models.CASCADE, related_name="dispositivos_cap", null="True")