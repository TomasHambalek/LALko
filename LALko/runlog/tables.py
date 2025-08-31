# runlog/tables.py

import django_tables2 as tables
from .models import Operation
from django.urls import reverse

class OperationTable(tables.Table):
    id = tables.LinkColumn(
        "operation_detail", 
        args=[tables.A("pk")],
        verbose_name="ID"
    )

    def render_operators(self, record):
        return ", ".join([str(o) for o in record.operators.all()])

    project_number = tables.Column(accessor="project_number__name", verbose_name="Project Number")
    aac_mold_number = tables.Column(accessor="aac_mold_number__name", verbose_name="AAC Mold Number")
    mold_number = tables.Column(verbose_name="Mold Number")
    surface = tables.Column(accessor="surface__name", verbose_name="Surface")
    moldset_preform = tables.Column(accessor="moldset_preform__name", verbose_name="Moldset Preform")
    operators = tables.Column(verbose_name="Operators")
    parent_layout = tables.Column(accessor="parent_layout__name", verbose_name="Parent Layout")
    machine = tables.Column(accessor="machine__name", verbose_name="Machine")
    machining_type = tables.Column(accessor="machining_type__name", verbose_name="Machining Type")
    status = tables.Column(accessor="status__name", verbose_name="Status")
    task = tables.Column(accessor="task__name", verbose_name="Task")

    start_time = tables.DateTimeColumn(verbose_name="Start Time")
    end_time = tables.DateTimeColumn(verbose_name="End Time")
    duration = tables.Column(verbose_name="Duration")
    x_levelling = tables.Column(verbose_name="X Levelling")
    y_levelling = tables.Column(verbose_name="Y Levelling")
    short_description = tables.Column(
        accessor="description", 
        verbose_name="Description",
        attrs={"th": {"style": "width: 250px;"}, "td": {"style": "max-width: 250px;"}}
    )
    note = tables.Column(
        verbose_name="Note",
        attrs={"th": {"style": "width: 150px;"}, "td": {"style": "max-width: 150px;"}}
    )
    note2 = tables.Column(
        verbose_name="Note2",
        attrs={"th": {"style": "width: 150px;"}, "td": {"style": "max-width: 150px;"}}
    )

    actions = tables.TemplateColumn(
        template_name="runlog/table_actions.html",
        verbose_name="Actions"
    )

    class Meta:
        model = Operation
        template_name = "django_tables2/bootstrap4.html"
        orderable = False
        order_by = ("-id",) 
        per_page = 50
        fields = (
            "id", "project_number", "aac_mold_number", "mold_number", "surface",
            "moldset_preform", "parent_layout", "machine", "machining_type", "operators", 
            "status", "task", "start_time", "end_time", "duration",
            "short_description", "x_levelling", "y_levelling", "note", "note2", "actions"
        )
        # Toto je opravená verze. Přidali jsme zpět třídy 'table' a 'table-striped'.
        attrs = {"class": "table table-striped table-bordered text-center"}