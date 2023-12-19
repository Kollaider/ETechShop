from rest_framework.viewsets import ReadOnlyModelViewSet
from api.filters import NetworkNodeFilter
from api.serializers import NetworkNodeSerializer, NetworkNodeDebtSerializer
from webapp.models import NetworkNode
from django.db.models import Avg, F
from rest_framework.decorators import action
from rest_framework.response import Response


class NetworkNodeViewSet(ReadOnlyModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filterset_class = NetworkNodeFilter
    filter_backends = ['product_id']
    ordering_fields = ['id']

    @action(detail=False, methods=['GET'])
    def debt_statistics(self, request):
        average_debt = NetworkNode.objects.aggregate(average_debt=Avg('debt'))['average_debt']
        nodes_with_high_debt = NetworkNode.objects.filter(debt__gt=average_debt)
        statistic = {
            'average_debt': average_debt,
            'network_nodes': NetworkNodeDebtSerializer(nodes_with_high_debt, many=True).data,
        }
        return Response(statistic)
