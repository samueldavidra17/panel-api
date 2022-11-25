from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat
from simple_history.models import HistoricalRecords

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
    estatus = models.CharField(max_length=45, default="OPERATIVA")
    asignacion = models.CharField(max_length=45, default="POR ASIGNAR")
    observacion = models.TextField(default="S/N")
    ubicaciones = models.ForeignKey(ubicaciones, on_delete=models.CASCADE, related_name="ubicacionesUser", default=1)
    # usuarios = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name="informacion_us", null="True")

class modelos(models.Model):
    nombre = models.CharField(max_length=45)
    tiposEquiposMarcas = models.ForeignKey(tipos_equipos_marcas, on_delete=models.CASCADE, related_name="tiposEquiposMarcasId", null="True")

class equipos(models.Model):
    id = models.OneToOneField(informacion, primary_key=True, unique=True, on_delete=models.CASCADE, related_name="informacion_eq", blank=True)
    empresas = models.ForeignKey(empresas, on_delete=models.CASCADE, related_name="empresasEq", null=True, default=1, blank=True)
    modelos = models.ForeignKey(modelos, on_delete=models.CASCADE, related_name="modelosEq", null=False, blank=True)
    serial = models.CharField(max_length=45, default="S/N", blank=True)
    serial_unidad = models.CharField(max_length=45, default="S/N", blank=True)
    serial_cargador = models.CharField(max_length=45, default="S/N", blank=True)
    csb= models.CharField(max_length=45, default="S/N", blank=True)
    dd = models.CharField(max_length=45, default="S/N", blank=True)
    ram = models.CharField(max_length=45, default="S/N", blank=True)
    tipo_ram = models.CharField(max_length=45, default="S/N", blank=True)
    antivirus = models.CharField(max_length=45, default="S/N", blank=True)
    so = models.CharField(max_length=45, default="S/N", blank=True)
    usuario_so = models.CharField(max_length=45, default="S/N", unique=True, blank=True)
    usuarios = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name="equiposUs", null=True, blank=True)
    history = HistoricalRecords()
    # historyUser = HistoricalRecords(excluded_fields=['empresas, modelos, serial, serial_unidad, serial_cargador, csb, dd, ram, tipo_ram, antivirus, so, usuarios_so, history'])

    # def __str__(self):
    #     return self.usuarios

    # def save(self, *args, **kwargs):
    #     if not self.pk and self.usuarios:
    #         self.usuarios.available
    #         self.usuarios.save()
    #     return super(equipos, self).save(*args, **kwargs)

class impresoras(models.Model):
    TIPOS_IMPRESIONES = (
        ('NO APLICA','No aplica'),
        ('CINTA','Cinta'),
        ('TONER','Toner'),
        ('RIBON','Ribon'),
        ('TINTA','Tinta')
    )
    TIPOS_CONEXION = (
        ('NO APLICA','No aplica'),
        ('RED','Red'),
        ('USB','Usb'),
        ('COMPARTIDA','Compartida')
    )
    tipo_impresion = models.CharField(max_length=45, choices=TIPOS_IMPRESIONES)
    serial = models.CharField(max_length=45)
    csb = models.CharField(max_length=45)
    toner = models.CharField(max_length=45)
    tipo_conexion = models.CharField(max_length=45, choices=TIPOS_CONEXION, default="No aplica")
    ip = models.CharField(max_length=45)
    departamento = models.ForeignKey(departamentos, on_delete=models.CASCADE, related_name="departamentosImpresora", null=False)
    id = models.OneToOneField(informacion, primary_key=True, unique=True, on_delete=models.CASCADE, related_name="informacion_imp", blank=True)
    modelos = models.ForeignKey(modelos, on_delete=models.CASCADE, related_name="modelosImp", null="True")

class dispositivos(models.Model):
    serial = models.CharField(max_length=45, default="S/N")
    csb = models.CharField(max_length=45, default="S/N")
    modelos = models.ForeignKey(modelos, on_delete=models.CASCADE, related_name="modelosDis", null="True")
    asignado = models.OneToOneField(equipos, to_field='usuario_so', on_delete=models.CASCADE, related_name="equiposDis", null="True")
    
