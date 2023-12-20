from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from api.filters import NetworkNodeFilter
from api.permissions import IsActiveEmployeePermission
from api.serializers import NetworkNodeSerializer, NetworkNodeDebtSerializer, ProductSerializer
from webapp.models import NetworkNode, Product, EmployeeProfileInfo
from django.db.models import Avg, F
from rest_framework.decorators import action
from rest_framework.response import Response
from webapp.tasks import generate_qr_code_and_send_email
from webapp.utils import generate_networknode_contact_info


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

    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data.pop('hierarchy_level', None)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        employees_data = request.data.get('employees', [])
        products_data = request.data.get('products', [])

        network_node = serializer.instance

        # Bulk retrieval of employees
        employees = EmployeeProfileInfo.objects.filter(id__in=employees_data)
        employee_ids = set(employee.id for employee in employees)

        # Check for missing employees
        missing_employees = set(employees_data) - employee_ids
        if missing_employees:
            return Response(
                {'error': f'Employees with IDs {", ".join(map(str, missing_employees))} do not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Bulk add employees to the network node
        network_node.employees.add(*employees)

        # Bulk retrieval of products
        products = Product.objects.filter(id__in=products_data)
        product_ids = set(product.id for product in products)

        # Check for missing products
        missing_products = set(products_data) - product_ids
        if missing_products:
            return Response(
                {'error': f'Products with IDs {", ".join(map(str, missing_products))} do not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Bulk add products to the network node
        network_node.products.add(*products)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    @action(detail=True, methods=['POST'])
    def send_netwoknode_info_email(self, request, pk):
        try:
            network_node = NetworkNode.objects.get(pk=int(pk))
            email, network_node_data  = generate_networknode_contact_info(network_node)

            generate_qr_code_and_send_email.delay(email, network_node_data)

            return Response({'message': 'QR code generation and email sending in progress'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'object with such pk not found'}, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Exclude hierarchy_level from request data
        request_data = request.data.copy()
        request_data.pop('hierarchy_level', None)

        serializer = self.get_serializer(instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        # Update employees
        employees_data = request_data.get('employees', [])
        employees = EmployeeProfileInfo.objects.filter(id__in=employees_data)
        employee_ids = set(employee.id for employee in employees)

        missing_employees = set(employees_data) - employee_ids
        if missing_employees:
            return Response(
                {'error': f'Employees with IDs {", ".join(map(str, missing_employees))} do not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.employees.set(employees)

        # Update products
        products_data = request_data.get('products', [])
        products = Product.objects.filter(id__in=products_data)
        product_ids = set(product.id for product in products)

        missing_products = set(products_data) - product_ids
        if missing_products:
            return Response(
                {'error': f'Products with IDs {", ".join(map(str, missing_products))} do not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.products.set(products)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
