# runlog/tables.py

import django_tables2 as tables
from .models import Operation
from django.urls import reverse

class OperationTable(tables.Table):
    id = tables.LinkColumn(
        "operation_detail", 
        args=[tables.A("pk")],
        verbose_name="ID",
        attrs={
            "a": {"class": "badge bg-success"},
            "th": {"style": "width: auto;"},
            "td": {"style": "max-width: auto;"}
        }
    )

    def render_operators(self, record):
        return ", ".join([str(o) for o in record.operators.all()])

    def render_duration(self, value):
        if value is None:
            return ""
        return f"{value:.2f}"

    project_number = tables.Column(
        accessor="project_number__name", 
        verbose_name="Project Number",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    aac_mold_number = tables.Column(
        accessor="aac_mold_number__name", 
        verbose_name="AAC Mold Number",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    mold_number = tables.Column(
        verbose_name="Mold Number",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    surface = tables.Column(
        accessor="surface__name", 
        verbose_name="Surface",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    moldset_preform = tables.Column(
        accessor="moldset_preform__name", 
        verbose_name="Moldset Preform",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    operators = tables.Column(
        verbose_name="Operators",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    parent_layout = tables.Column(
        accessor="parent_layout__name", 
        verbose_name="Parent Layout",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    machine = tables.Column(
        accessor="machine__name", 
        verbose_name="Machine",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    machining_type = tables.Column(
        accessor="machining_type__name", 
        verbose_name="Machining Type",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    status = tables.Column(
        accessor="status__name", 
        verbose_name="Status",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    task = tables.Column(
        verbose_name="Task",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )

    start_time = tables.DateTimeColumn(
        verbose_name="Start Time",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    end_time = tables.DateTimeColumn(
        verbose_name="End Time",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    duration = tables.Column(
        verbose_name="Duration",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    x_levelling = tables.Column(
        verbose_name="X Levelling",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    y_levelling = tables.Column(
        verbose_name="Y Levelling",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
    )
    short_description = tables.Column(
        accessor="description", 
        verbose_name="Description",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: 200px;"}}
    )
    note = tables.Column(
        verbose_name="Note",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: 200px;"}}
    )
    note2 = tables.Column(
        verbose_name="Note2",
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: 200px;"}}
    )

    actions = tables.TemplateColumn(
        template_name="runlog/table_actions.html",
        verbose_name="Actions",
        visible=False,
        attrs={"th": {"style": "width: auto;"}, "td": {"style": "max-width: auto;"}}
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
        # Zde kombinujeme třídy a styl šířky
        attrs = {"class": "table table-striped table-bordered text-center align-middle", "style": "width: 100%;"}
        th_attrs = {"class": "text-center align-middle"}