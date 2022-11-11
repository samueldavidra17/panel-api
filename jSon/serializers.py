from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.http import HttpResponse
from .models import asignaciones, estatus, tiposRam, so

class asignacionesSerializers(serializers.ModelSerializer):
    class Meta:
        model = asignaciones
        fields = ('id','nombre')

class estatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = estatus
        fields = ('id','nombre')

class tiposRamSerializers(serializers.ModelSerializer):
    class Meta:
        model = tiposRam
        fields = ('id','nombre')

    
class soSerializers(serializers.ModelSerializer):
    class Meta:
        model = so
        fields = ('id','nombre')

class asignacionesMinSerializers(serializers.ModelSerializer):
    class Meta:
        model = asignaciones
        fields = ('id','nombre')

    def to_representation(self, value):
        return value.nombre

class estatusMinSerializers(serializers.ModelSerializer):
    class Meta:
        model = estatus
        fields = ('id','nombre')

    def to_representation(self, value):
        return value.nombre

class tiposRamMinSerializers(serializers.ModelSerializer):
    class Meta:
        model = tiposRam
        fields = ('id','nombre')

    def to_representation(self, value):
        return value.nombre

class soMinSerializers(serializers.ModelSerializer):
    class Meta:
        model = so
        fields = ('id','nombre')

    def to_representation(self, value):
        return value.nombre
        
    # def create(self, validated_data):
    #     return so.objects.create(**validated_data)