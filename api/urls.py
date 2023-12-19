from django.urls import include, path
from rest_framework import routers

from api.views import NetworkNodeViewSet


router = routers.DefaultRouter()
router.register(r'network_nodes', NetworkNodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += router.urls
