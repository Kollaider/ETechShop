from webapp.models import NetworkNode
from django_filters import rest_framework as filters


class NetworkNodeFilter(filters.FilterSet):
    country = filters.CharFilter(
        field_name='contact__address__country',
        lookup_expr="iexact"
    )

    class Meta:
        model = NetworkNode
        fields = ['contact__address__country']
