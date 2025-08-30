# runlog/filters.py

import django_filters
from django import forms
from .models import (
    Operation, AACMoldNumber, Machine, MachiningType, MoldsetPreform,
    Operator, ParentLayout, ProjectNumber, Status, Surface, Task
)

class OperationFilter(django_filters.FilterSet):
    project_number = django_filters.ModelChoiceFilter(
        queryset=ProjectNumber.objects.all(),
        label="Project Number",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    aac_mold_number = django_filters.ModelChoiceFilter(
        queryset=AACMoldNumber.objects.all(),
        label="AAC Mold Number",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    mold_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Mold Number",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    surface = django_filters.ModelChoiceFilter(
        queryset=Surface.objects.all(),
        label="Surface",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    moldset_preform = django_filters.ModelChoiceFilter(
        queryset=MoldsetPreform.objects.all(),
        label="Moldset Preform",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    parent_layout = django_filters.ModelChoiceFilter(
        queryset=ParentLayout.objects.all(),
        label="Parent Layout",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    machine = django_filters.ModelChoiceFilter(
        queryset=Machine.objects.all(),
        label="Machine",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    machining_type = django_filters.ModelChoiceFilter(
        queryset=MachiningType.objects.all(),
        label="Machining Type",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    operators = django_filters.ModelMultipleChoiceFilter(
        queryset=Operator.objects.all(),
        label="Operators",
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Status",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    task = django_filters.ModelChoiceFilter(
        queryset=Task.objects.all(),
        label="Task",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    description = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Description",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    start_time = django_filters.DateTimeFilter(
        lookup_expr='gte',
        label="Start Time (from)",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    end_time = django_filters.DateTimeFilter(
        lookup_expr='lte',
        label="End Time (to)",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    x_levelling = django_filters.NumberFilter(
        label="X Levelling",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    y_levelling = django_filters.NumberFilter(
        label="Y Levelling",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    note = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Note",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    note2 = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Note 2",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Operation
        # DŮLEŽITÉ: Nyní je seznam polí vyplněn
        fields = [
            'project_number', 'aac_mold_number', 'mold_number', 'surface',
            'moldset_preform', 'parent_layout', 'machine', 'machining_type',
            'operators', 'status', 'task', 'description', 'start_time',
            'end_time', 'x_levelling', 'y_levelling', 'note', 'note2'
        ]