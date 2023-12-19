from django.contrib import admin

from webapp.models import NetworkNode, EmployeeProfileInfo, Product, ContactInfo, Address


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'network_level', 'hierarchy_level', 'supplier')
    readonly_fields = ('hierarchy_level',)


@admin.register(EmployeeProfileInfo)
class EmployeeProfileInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    pass

