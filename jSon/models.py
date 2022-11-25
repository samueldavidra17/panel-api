from django.db import models
        
class asignaciones(models.Model):
    nombre = models.CharField(max_length=50)

class estatus(models.Model):
    nombre = models.CharField(max_length=50)

class tiposRam(models.Model):
    nombre = models.CharField(max_length=50)

class so(models.Model):
    nombre = models.CharField(max_length=50)
