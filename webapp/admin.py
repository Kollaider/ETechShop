from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe

from webapp.models import NetworkNode, EmployeeProfileInfo, Product, Contact, Address
from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import NetworkNode




class NetworkNodeForm(forms.ModelForm):
    class Meta:
        model = NetworkNode
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if there's a supplier
        if self.instance.supplier:
            supplier_url = reverse('admin:webapp_networknode_change', args=[self.instance.supplier.id])
            supplier_link = format_html('<a href="{}">{}</a>', supplier_url, self.instance.supplier.name)
            self.fields['supplier_link'] = forms.CharField(
                label='Supplier',
                initial=supplier_link,
                disabled=True,
                required=False
            )


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):

    list_display = ('name', 'network_level', 'hierarchy_level', 'created_at')
    list_filter = ('network_level',)
    search_fields = ('name',)
    readonly_fields = ('hierarchy_level', 'created_at')
    filter_horizontal = ('products', 'employees',)

    fieldsets = (
        (None, {
            'fields': ('name', 'network_level', 'hierarchy_level', 'debt', 'created_at')
        }),
        ('Supplier', {
            'fields': ('supplier', 'supplier_link'),
        }),
        ('Other Fields', {
            'fields': ('contact', 'products', 'employees'),
        }),
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj.supplier:
            supplier_link = reverse('admin:webapp_networknode_change', args=[obj.supplier.id])
            supplier_link = format_html('<a href="{}">{}</a>', supplier_link, obj.supplier.name)
        else:
            supplier_link = "N/A"  # or any other text you prefer

        self.readonly_fields += ('supplier_link',)  # Add supplier_link to readonly_fields

        return super().change_view(request, object_id, form_url, extra_context)

    def supplier_link(self, obj):
        if obj.supplier:
            supplier_link = reverse('admin:webapp_networknode_change', args=[obj.supplier.id])
            return mark_safe(format_html('<a href="{}">{}</a>', supplier_link, obj.supplier.name))
        else:
            return "N/A"

    supplier_link.short_description = "Supplier Link"  # Set a custom column header

    # Remove 'supplier' from readonly_fields since we're using 'supplier_link' now
    readonly_fields = tuple(field for field in readonly_fields if field != 'supplier')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'street', 'house_number')




@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'address')


@admin.register(EmployeeProfileInfo)
class EmployeeProfileInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'birth_date', 'address')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')
