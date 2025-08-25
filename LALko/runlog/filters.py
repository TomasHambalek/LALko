# runlog/filters.py
import django_filters
from .models import Operation
    
class OperationFilter(django_filters.FilterSet):
    # Přidáváme pole, které chceme filtrovat
    operator_name = django_filters.CharFilter(
        field_name='operator__name',  # Odkazuje na 'name' v modelu 'Operator'
        lookup_expr='icontains',       # Povoluje hledání podle části řetězce (case-insensitive)
        label='Operator Name'
    )

    class Meta:
        model = Operation
        fields = {
            'project_number__name': ['exact', 'icontains'],
            # 'operator__name' již není potřeba zde, protože je definováno výše
            'machine__name': ['exact', 'icontains'],
            'status__name': ['exact', 'icontains'],
            'task__name': ['exact', 'icontains'],
        }