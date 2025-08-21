# runlog/admin.py

from django.contrib import admin
from .models import Machine, MachiningType, Task, Operator, Operation, Project, Status

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

@admin.register(MachiningType)
class MachiningTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("task_name", "status")
    search_fields = ("task_name", "status")
    list_filter = ("status",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_number", "aac_mold_number", "mold_number", "surface", "moldset", "preform", "layout")
    search_fields = ("project_number", "aac_mold_number", "mold_number")
    list_filter = ("surface", "layout")

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    # Opraveno: "get_operators" bylo změněno na "get_operator_name"
    list_display = ("id", "project", "task", "machine", "machining_type", "get_operator_name")
    search_fields = ("project__project_number", "task__task_name", "operator__name")
    list_filter = ("machine", "machining_type", "task__status")

    def get_operator_name(self, obj):
        return obj.operator.name if obj.operator else "N/A"
    get_operator_name.short_description = "Operator"