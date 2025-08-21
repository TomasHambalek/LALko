# runlog/forms.py

from django import forms
from .models import Operation, Task # Ujistěte se, že importujete Task

class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = [
            'project', 'task', 'machine', 'machining_type', 'operator', 'status',
            'x_levelling', 'y_levelling', 'start_time', 'end_time',
            'note', 'note2'
        ]