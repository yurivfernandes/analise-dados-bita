import django_filters

from ...models import DeviceInventario


class DeviceInventarioFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )
    sigla = django_filters.CharFilter(
        field_name="sigla", lookup_expr="icontains"
    )
    model = django_filters.CharFilter(
        field_name="model", lookup_expr="icontains"
    )
    organization_id = django_filters.NumberFilter(field_name="organization_id")
    status_migrado = django_filters.BooleanFilter(
        method="filter_status_migrado"
    )

    class Meta:
        model = DeviceInventario
        fields = [
            "name",
            "sigla",
            "model",
            "organization_id",
            "status_migrado",
        ]

    def filter_status_migrado(self, queryset, name, value):
        return (
            queryset.filter(**{name: value})
            if isinstance(value, bool)
            else queryset
        )
