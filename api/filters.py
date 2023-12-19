from webapp.models import NetworkNode
from django_filters import rest_framework as filters


class NetworkNodeFilter(filters.FilterSet):
    country = filters.CharFilter(
        field_name='contact__address__country',
        lookup_expr='exact'
    )

    product_id = filters.NumberFilter(
        field_name='products__id',
        lookup_expr='exact'
    )

    class Meta:
        model = NetworkNode
        fields = [
            'contact__address__country',
            'product_id'
        ]
