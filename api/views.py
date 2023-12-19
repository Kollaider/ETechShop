from rest_framework.viewsets import ReadOnlyModelViewSet
from api.filters import NetworkNodeFilter
from api.serializers import NetworkNodeSerializer
from webapp.models import NetworkNode


class NetworkNodeViewSet(ReadOnlyModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filterset_class = NetworkNodeFilter
    ordering_fields = ['id']
