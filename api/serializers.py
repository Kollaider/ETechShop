from rest_framework import serializers

from webapp.models import NetworkNode, Contact, Address, EmployeeProfileInfo, Product



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class EmployeeProfileInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeProfileInfo
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Contact
        fields = '__all__'


class NetworkNodeSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    employees = EmployeeProfileInfoSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = '__all__'
        read_only_fields = ['hierarchy_level']

    def validate(self, data):
        supplier = data.get('supplier')
        network_level = data.get('network_level')
        debt = data.get('debt')
        instance = self.instance

        if supplier and network_level <= supplier.network_level:
            raise serializers.ValidationError("Network level must be higher than the supplier's network level.")

        if debt < 0:
            raise serializers.ValidationError("Debt amount must be a positive number.")

        if instance is None and debt is None:
            return data
        elif instance and debt is not None and instance.debt != debt:
            raise serializers.ValidationError("Changing the debt field during an update is not allowed.")

        if instance and supplier.id == instance.id:
            raise serializers.ValidationError("Recursive supplier-child relationship is not allowed.")

        return data


class NetworkNodeDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = ('id', 'debt', 'name')


class DebtStatisticSerializer(serializers.Serializer):
    average_debt = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    network_nodes = NetworkNodeDebtSerializer(many=True, read_only=True)