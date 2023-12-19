from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from api.filters import NetworkNodeFilter
from api.permissions import IsActiveEmployeePermission
from api.serializers import NetworkNodeSerializer, NetworkNodeDebtSerializer, ProductSerializer
from webapp.models import NetworkNode, Product
from django.db.models import Avg, F
from rest_framework.decorators import action
from rest_framework.response import Response


class NetworkNodeViewSet(ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filterset_class = NetworkNodeFilter
    permission_classes = [IsAuthenticated, IsActiveEmployeePermission]
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


#     def create(self, request, *args, **kwargs):
#         serializer = NetworkNodeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class ProductViewSet(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
