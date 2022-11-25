from rest_framework import routers

from .api import asignacionesViewSet

router = routers.DefaultRouter()

router.register('asignaciones',asignacionesViewSet, 'asignaciones')

urlpatterns = router.urls