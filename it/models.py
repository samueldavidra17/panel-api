from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat
from simple_history.models import HistoricalRecords

# Create your models here.
# DOCUMENTACIO
# Creacion de los modelos que se migran a la base de dato
# related_name hace referencia a un dato de una tabla traido de otra tabla
# through es el dato para mandar a la relacion de muchos a muchos para que así se relacionen dos tablas con una auxiliar

class empresas(models.Model):
    nombre = models.CharField(max_length=45)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(empresas, self).save( *args, **kwargs)

class marcas(models.Model):
    nombre = models.CharField(max_length=45)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(marcas, self).save( *args, **kwargs)

class tipos_equipos(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=45)
    marcas = models.ManyToManyField(marcas, related_name="tiposEquiposMarcas", through="tipos_equipos_marcas")

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(tipos_equipos, self).save( *args, **kwargs)
    # def Test(request):
    #  query = tipos_equipos.objects.annotate(C=Concat('1',Value('-') ,'2',
    #              output_field=CharField()))

class tipos_equipos_marcas(models.Model):
    marcas = models.ForeignKey(marcas, on_delete=models.CASCADE, related_name="marcasId", null="True")
    tiposEquipos = models.ForeignKey(tipos_equipos, on_delete=models.CASCADE, related_name="tiposEquiposId", null="True")

class departamentos(models.Model):
    nombre = models.CharField(max_length=45)
    empresas = models.ManyToManyField(empresas, related_name="empresasDepartamentos", through="departamentos_empresas")

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(departamentos, self).save( *args, **kwargs)

class departamentos_empresas(models.Model):
    departamentos = models.ForeignKey(departamentos, on_delete=models.CASCADE, related_name="empresasId", null=False)
    empresas = models.ForeignKey(empresas, on_delete=models.CASCADE, related_name="departamentosId", null=False)
    
class ubicaciones(models.Model):
    nombre = models.CharField(max_length=45)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(ubicaciones, self).save( *args, **kwargs)

class usuarios(models.Model):
    nombre = models.CharField(max_length=45)
    cargo = models.CharField(max_length=45)
    departamentosEmpresas = models.ForeignKey(departamentos_empresas, on_delete=models.CASCADE, related_name="departamentoEmpresaUs", null=False)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.cargo = self.cargo.upper()
        super(informacion, self).save( *args, **kwargs)

class informacion(models.Model):
    estatus = models.CharField(max_length=45, default="OPERATIVA")
    asignacion = models.CharField(max_length=45, default="POR ASIGNAR")
    observacion = models.TextField(default="S/N")
    ubicaciones = models.ForeignKey(ubicaciones, on_delete=models.CASCADE, related_name="ubicacionesUser", default=1)

    def save(self, *args, **kwargs):
        self.estatus = self.estatus.upper()
        self.asignacion = self.asignacion.upper()
        self.observacion = self.observacion.upper()
        super(informacion, self).save( *args, **kwargs)

class modelos(models.Model):
    nombre = models.CharField(max_length=45)
    tiposEquiposMarcas = models.ForeignKey(tipos_equipos_marcas, on_delete=models.CASCADE, related_name="tiposEquiposMarcasId", null="True")

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(modelos, self).save( *args, **kwargs)

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
    usuario_so = models.CharField(max_length=45, unique=True, null=True)
    usuarios = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name="equiposUs", null=True, blank=True)
    #Para crear la bitacora o historial se usa esto, investigar para mayor información django-simple-history
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.antivirus = self.antivirus.upper()
        self.so = self.so.upper()
        self.serial = self.serial.upper()
        self.serial_unidad = self.serial_unidad.upper()
        self.serial_cargador = self.serial_cargador.upper()
        self.csb = self.csb.upper()
        self.usuario_so = self.usuario_so.upper() if self.usuario_so is not None else self.usuario_so
        super(equipos, self).save( *args, **kwargs) # Call the "real" save() method.
    # historyUser = HistoricalRecords(excluded_fields=['empresas, modelos, serial, serial_unidad, serial_cargador, csb, dd, ram, tipo_ram, antivirus, so, usuarios_so, history'])

class impresoras(models.Model):
    TIPOS_CONEXION = (
        ('NO APLICA','No aplica'),
        ('RED','Red'),
        ('USB','Usb'),
        ('COMPARTIDA','Compartida')
    )
    id = models.OneToOneField(informacion, primary_key=True, unique=True, on_delete=models.CASCADE, related_name="informacion_imp", blank=True)
    serial = models.CharField(max_length=45, default="S/N")
    csb = models.CharField(max_length=45, default="S/N")
    toner = models.CharField(max_length=45)
    tipo_conexion = models.CharField(max_length=45, choices=TIPOS_CONEXION, default="No aplica")
    ip = models.CharField(max_length=45, default="No aplica")
    departamento = models.ForeignKey(departamentos, on_delete=models.CASCADE, related_name="departamentosImpresora", null=False)
    modelos = models.ForeignKey(modelos, on_delete=models.CASCADE, related_name="modelosImp", null="True")

    def save(self, *args, **kwargs):
        self.serial = self.serial.upper()
        self.csb = self.csb.upper()
        self.toner = self.toner.upper()
        self.tipo_conexion = self.tipo_conexion.upper()
        super(impresoras, self).save( *args, **kwargs)

class dispositivos(models.Model):
    serial = models.CharField(max_length=45, default="S/N")
    csb = models.CharField(max_length=45, default="S/N")
    modelos = models.ForeignKey(modelos, on_delete=models.CASCADE, related_name="modelosDis", null="True")
    asignado = models.OneToOneField(equipos, to_field='usuario_so', on_delete=models.CASCADE, related_name="equiposDis", null="True")

    def save(self, *args, **kwargs):
        self.serial = self.serial.upper()
        self.csb = self.csb.upper()
        super(informacion, self).save( *args, **kwargs)
    
