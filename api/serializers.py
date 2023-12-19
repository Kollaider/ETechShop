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
    contact = ContactSerializer()
    employees = EmployeeProfileInfoSerializer(many=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = NetworkNode
        fields = '__all__'
