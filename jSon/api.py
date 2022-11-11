from .models import asignaciones, tiposRam, so, estatus
from .serializers import asignacionesSerializers
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response

class asignacionesViewSet(viewsets.ModelViewSet):
    queryset = asignaciones.objects.using('json_db')
    permission_classes = [permissions.AllowAny]
    serializer_class = asignacionesSerializers

    # serializer_class = asignacionesSerializers

    # def get_queryset(self):
    #     queryset = asignaciones.objects.using('json_db')
    #     serializer = asignacionesSerializers(queryset)
    #     if queryset:
    #         return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = ResourceSerializer(data=request.DATA, many=True)
    #     if serializer.is_valid():
    #         serializer.save(using='json_db')
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)