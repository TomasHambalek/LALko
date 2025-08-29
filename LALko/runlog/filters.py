# runlog/filters.py
import django_filters
from .models import (
    Operation, AACMoldNumber, Machine, MachiningType, MoldsetPreform,
    Operator, ParentLayout, ProjectNumber, Status, Surface, Task
)

class OperationFilter(django_filters.FilterSet):
    # Přidání filtru pro ID
    id = django_filters.NumberFilter(label="ID")

    project_number = django_filters.ModelChoiceFilter(queryset=ProjectNumber.objects.all(), label="Project Number")
    aac_mold_number = django_filters.ModelChoiceFilter(queryset=AACMoldNumber.objects.all(), label="AAC Mold Number")
    mold_number = django_filters.CharFilter(lookup_expr='icontains', label="Mold Number")
    surface = django_filters.ModelChoiceFilter(queryset=Surface.objects.all(), label="Surface")
    moldset_preform = django_filters.ModelChoiceFilter(queryset=MoldsetPreform.objects.all(), label="Moldset Preform")
    parent_layout = django_filters.ModelChoiceFilter(queryset=ParentLayout.objects.all(), label="Parent Layout")
    machine = django_filters.ModelChoiceFilter(queryset=Machine.objects.all(), label="Machine")
    machining_type = django_filters.ModelChoiceFilter(queryset=MachiningType.objects.all(), label="Machining Type")
    
    # OPRAVENÝ ŘÁDEK: Změna z ModelChoiceFilter na ModelMultipleChoiceFilter a z "operator" na "operators"
    operators = django_filters.ModelMultipleChoiceFilter(queryset=Operator.objects.all(), label="Operators")
    
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all(), label="Status")
    task = django_filters.ModelChoiceFilter(queryset=Task.objects.all(), label="Task")

    # Přidání filtru pro duration
    duration = django_filters.NumberFilter(label="Duration (hours)")

    # Ostatní pole, která nejsou cizí klíče
    start_time = django_filters.DateTimeFilter(lookup_expr='gte', label="Start Time (from)")
    end_time = django_filters.DateTimeFilter(lookup_expr='lte', label="End Time (to)")
    x_levelling = django_filters.NumberFilter(label="X Levelling")
    y_levelling = django_filters.NumberFilter(label="Y Levelling")
    note = django_filters.CharFilter(lookup_expr='icontains', label="Note")
    note2 = django_filters.CharFilter(lookup_expr='icontains', label="Note 2")

    # Pro pole description použijeme CharFilter s icontains pro vyhledávání
    description = django_filters.CharFilter(lookup_expr='icontains', label="Description")

    class Meta:
        model = Operation
        fields = []