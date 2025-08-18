from django import forms
from .models import Operation

class OperationForm(forms.ModelForm):
    """Form to create a new operation entry."""
    class Meta:
        model = Operation
        fields = "__all__"
