from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
# DOCUMENTACIO
# Creacion de los modelos que se migran a la base de dato
# related_name hace referencia a un dato de una tabla traido de otra tabla
# through es el dato para mandar a la relacion de muchos a muchos para que así se relacionen dos tablas con una auxiliar

class Empresas(models.Model):
    nombre = models.CharField(max_length=45)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Empresas, self).save( *args, **kwargs)

class Departamentos(models.Model):
    nombre = models.CharField(max_length=45)
    empresas = models.ManyToManyField(Empresas, related_name="empresasDepartamentos", through="DepartamentosEmpresas")

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Departamentos, self).save( *args, **kwargs)

class DepartamentosEmpresas(models.Model):
    departamentos = models.ForeignKey(Departamentos, on_delete=models.CASCADE, related_name="empresasId", null=False)
    empresas = models.ForeignKey(Empresas, on_delete=models.CASCADE, related_name="departamentosId", null=False)

    class Meta:
        db_table = 'inventario_departamentos_empresas'
        
class Usuarios(models.Model):
    nombre = models.CharField(max_length=45)
    cargo = models.CharField(max_length=45)
    departamentosEmpresas = models.ForeignKey(DepartamentosEmpresas, on_delete=models.CASCADE, related_name="departamentoEmpresaUs", null=False)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.cargo = self.cargo.upper()
        super(Usuarios, self).save(*args, **kwargs)

class Marcas(models.Model):
    nombre = models.CharField(max_length=45)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Marcas, self).save( *args, **kwargs)

class TiposEquipos(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=45)
    marcas = models.ManyToManyField(Marcas, related_name="tiposEquiposMarcas", through="TiposEquiposMarcas")

    class Meta:
        db_table = 'inventario_tipos_equipos'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(TiposEquipos, self).save( *args, **kwargs)

class TiposEquiposMarcas(models.Model):
    marcas = models.ForeignKey(Marcas, on_delete=models.CASCADE, related_name="marcasId", null="True")
    tiposEquipos = models.ForeignKey(TiposEquipos, on_delete=models.CASCADE, related_name="tiposEquiposId", null="True")

    class Meta:
        db_table = 'inventario_tipos_equipos_marcas'

class Modelos(models.Model):
    nombre = models.CharField(max_length=45)
    tiposEquiposMarcas = models.ForeignKey(TiposEquiposMarcas, on_delete=models.CASCADE, related_name="tiposEquiposMarcasId", null="True")

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Modelos, self).save( *args, **kwargs)
    
class Ubicaciones(models.Model):
    nombre = models.CharField(max_length=45)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Ubicaciones, self).save( *args, **kwargs)
    
class Asignaciones(models.Model):
    nombre = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Asignaciones, self).save( *args, **kwargs)

class Estatus(models.Model):
    nombre = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Estatus, self).save( *args, **kwargs)

class Estado(models.Model):
    asignacion = models.ForeignKey(Asignaciones, on_delete=models.CASCADE, related_name="asignacionEq", default=1)
    estatu = models.ForeignKey(Estatus, on_delete=models.CASCADE, related_name="estatusEq", default=1)
    ubicaciones = models.ForeignKey(Ubicaciones, on_delete=models.CASCADE, related_name="ubicacionEq", default=1)
    observacion = models.TextField(default="S/N")

    def save(self, *args, **kwargs):
        self.observacion = self.observacion.upper()
        super(Estado, self).save( *args, **kwargs)

class TiposRam(models.Model):
    nombre = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(TiposRam, self).save( *args, **kwargs)

    class Meta:
        db_table = 'inventario_tipos_ram'

class So(models.Model):
    nombre = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(So, self).save( *args, **kwargs)

class Equipos(models.Model):
    id = models.OneToOneField(Estado, primary_key=True, unique=True, on_delete=models.CASCADE, related_name="estadoEq", blank=True)
    nombre = models.CharField(max_length=45, null=True)
    empresas = models.ForeignKey(Empresas, on_delete=models.CASCADE, related_name="empresasEq", null=True, default=1, blank=True)
    modelo = models.ForeignKey(Modelos, on_delete=models.CASCADE, related_name="modeloEq", null=False, blank=True)
    serial = models.CharField(max_length=45, default="S/N", blank=True)
    serial_unidad = models.CharField(max_length=45, default="S/N", blank=True)
    serial_cargador = models.CharField(max_length=45, default="S/N", blank=True)
    csb= models.CharField(max_length=45, default="S/N", blank=True)
    dd = models.CharField(max_length=45, default="S/N", blank=True)
    ram = models.CharField(max_length=45, default="S/N", blank=True)
    tipo_ram = models.ForeignKey(TiposRam, on_delete=models.CASCADE, related_name="tipoRamEq", null=True, blank=True)
    so = models.ForeignKey(So, on_delete=models.CASCADE, related_name="soEq", null=True, blank=True)
    antivirus = models.CharField(max_length=45, default="S/N", blank=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name="usuarioEq", null=True, blank=True)
    #Para crear la bitacora o historial se usa esto, investigar para mayor información django-simple-history
    history = HistoricalRecords(table_name='inventario_equipos_historial')

    def save(self, *args, **kwargs):
        self.antivirus = self.antivirus.upper()
        self.serial = self.serial.upper()
        self.serial_unidad = self.serial_unidad.upper()
        self.serial_cargador = self.serial_cargador.upper()
        self.csb = self.csb.upper()
        self.nombre = self.nombre.upper() if self.nombre is not None else self.nombre
        super(Equipos, self).save( *args, **kwargs) # Call the "real" save() method.

    def save_without_history(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

class Impresoras(models.Model):
    TIPOS_CONEXION = (
        ('NO APLICA','No aplica'),
        ('RED','Red'),
        ('USB','Usb'),
        ('COMPARTIDA','Compartida')
    )
    id = models.OneToOneField(Estado, primary_key=True, unique=True, on_delete=models.CASCADE, related_name="estado_imp", blank=True)
    serial = models.CharField(max_length=45, default="S/N")
    csb = models.CharField(max_length=45, default="S/N")
    toner = models.CharField(max_length=45)
    tipo_conexion = models.CharField(max_length=45, choices=TIPOS_CONEXION, default="No aplica")
    ip = models.CharField(max_length=45, default="No aplica")
    departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE, related_name="departamentosImpresora", null=False)
    modelos = models.ForeignKey(Modelos, on_delete=models.CASCADE, related_name="modelosImp", null="True")

    def save(self, *args, **kwargs):
        self.serial = self.serial.upper()
        self.csb = self.csb.upper()
        self.toner = self.toner.upper()
        self.tipo_conexion = self.tipo_conexion.upper()
        super(Impresoras, self).save( *args, **kwargs)

class Dispositivos(models.Model):
    serial = models.CharField(max_length=45, default="S/N")
    csb = models.CharField(max_length=45, default="S/N")
    modelos = models.ForeignKey(Modelos, on_delete=models.CASCADE, related_name="modelosDis", null="True")
    asignado = models.OneToOneField(Equipos, on_delete=models.CASCADE, related_name="equiposDis", null="True")

    def save(self, *args, **kwargs):
        self.serial = self.serial.upper()
        self.csb = self.csb.upper()
        super(Dispositivos, self).save( *args, **kwargs)