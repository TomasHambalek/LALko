from django.contrib import admin
from .models import Machine, MachiningType, Task, Project, Operator, Operation

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
    list_display = ("user",)
    search_fields = ("user__username",)

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "task", "machine", "machining_type", "get_operators")
    search_fields = ("project__project_number", "task__task_name", "operators__user__username")
    list_filter = ("machine", "machining_type", "task__status")

    def get_operators(self, obj):
        return ", ".join([op.user.username for op in obj.operators.all()])
    get_operators.short_description = "Techniciens"
