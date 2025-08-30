# runlog/forms.py

from django import forms
from .models import Operation, AACMoldNumber, Machine, MachiningType, MoldsetPreform, Operator, ParentLayout, ProjectNumber, Status, Surface, Task

class OperationForm(forms.ModelForm):
    # Přepisujeme pole operators, abychom přidali help_text a widget
    operators = forms.ModelMultipleChoiceField(
        queryset=Operator.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Operators",
        help_text="(for selecting more press CTRL)"
    )

    class Meta:
        model = Operation
        fields = [
            # Všechna nová pole s ForeignKey
            "aac_mold_number",
            "machine",
            "machining_type",
            "mold_number",
            "moldset_preform",
            "operators",  # Použijeme přepsané pole
            "parent_layout",
            "project_number",
            "status",
            "surface",
            "task",
            "description",
            "x_levelling",
            "y_levelling",
            "start_time",
            "end_time",
            "note",
            "note2"
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'note2': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'x_levelling': forms.NumberInput(attrs={'class': 'form-control'}),
            'y_levelling': forms.NumberInput(attrs={'class': 'form-control'}),
        }