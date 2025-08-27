# runlog/forms.py

from django import forms
from .models import Operation, AACMoldNumber, Machine, MachiningType, MoldNumber, MoldsetPreform, Operator, ParentLayout, ProjectNumber, Status, Surface, Task

class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = [
            # Všechna nová pole s ForeignKey
            "aac_mold_number",
            "machine",
            "machining_type",
            "mold_number",
            "moldset_preform",
            "operators",
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