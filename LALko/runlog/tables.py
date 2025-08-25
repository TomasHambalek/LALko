# runlog/tables.py
import django_tables2 as tables
from .models import Operation
from django.urls import reverse

class OperationTable(tables.Table):
    # Vytvoříme sloupec 'ID' jako odkaz
    id = tables.LinkColumn(
        'operation_detail',  # Název URL cesty z urls.py
        args=[tables.A('pk')],  # Zajišťuje, že se jako argument předá primární klíč (pk)
        verbose_name="ID"
    )

    # Ostatní sloupce zůstávají stejné
    project_number = tables.Column(accessor="project_number__name", verbose_name="Project Number")
    aac_mold_number = tables.Column(accessor="aac_mold_number__name", verbose_name="AAC Mold Number")
    mold_number = tables.Column(accessor="mold_number__name", verbose_name="Mold Number")
    surface = tables.Column(accessor="surface__name", verbose_name="Surface")
    machine = tables.Column(accessor="machine__name", verbose_name="Machine")
    operator = tables.Column(accessor="operator__name", verbose_name="Operator")
    status = tables.Column(accessor="status__name", verbose_name="Status")
    task = tables.Column(accessor="task__name", verbose_name="Task")

    start_time = tables.DateTimeColumn(verbose_name="Start Time")
    end_time = tables.DateTimeColumn(verbose_name="End Time")
    duration = tables.Column(verbose_name="Duration (hours)")
    short_description = tables.Column(accessor="description", verbose_name="Description")
    
    class Meta:
        model = Operation
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "project_number", "aac_mold_number", "mold_number", "surface", "machine", "operator", "status", "task", "start_time", "end_time", "duration", "short_description")