from rest_framework.viewsets import ReadOnlyModelViewSet
from api.serializers import NetworkNodeSerializer
from webapp.models import NetworkNode


class NetworkNodeViewSet(ReadOnlyModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
