from django.contrib import admin
from .models import (
    AACMoldNumber, Machine, MachiningType, MoldNumber, MoldsetPreform,
    Operator, ParentLayout, ProjectNumber, Status, Surface, Task, Operation
)

# Registrace všech modelů
@admin.register(AACMoldNumber)
class AACMoldNumberAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(MachiningType)
class MachiningTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(MoldNumber)
class MoldNumberAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(MoldsetPreform)
class MoldsetPreformAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(ParentLayout)
class ParentLayoutAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(ProjectNumber)
class ProjectNumberAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Surface)
class SurfaceAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name",)

# Upravená třída pro Operations
@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_aac_mold_number",
        "get_machine",
        "get_machining_type",
        "get_mold_number",
        "get_moldset_preform",
        "get_operator",
        "get_parent_layout",
        "get_project_number",
        "get_surface",
        "get_status",
        "get_task",
        "start_time",
        "end_time",
        "duration",
        "get_description_short",  # Zkrácená verze description
        "get_note_short",         # Zkrácená verze note
        "get_note2_short",        # Zkrácená verze note2
        "x_levelling",
        "y_levelling",
    )
    #DOPLNIT
    search_fields = (
        "project_number__name",
        "aac_mold_number__name",
        "mold_number__name",
        "surface__name",
        "moldset_preform__name",
        "parent_layout__name",
        "machine__name",
        "machining_type__name",
        "operator__name",
        "status__name",
        "task__name",
        "description",
        "note",
        "note2",
    )
    #DOPLNIT
    list_filter = (
        "project_number",
        "aac_mold_number",
        "mold_number",
        "surface",
        "moldset_preform",
        "parent_layout",
        "machine",
        "machining_type",
        "operators",
        "status",
        "task",
    )

    # Pomocné metody pro zkrácení textových polí
    def get_description_short(self, obj):
        return obj.description[:20] + "..." if obj.description and len(obj.description) > 20 else obj.description
    get_description_short.short_description = "Description"
    
    def get_note_short(self, obj):
        return obj.note[:20] + "..." if obj.note and len(obj.note) > 20 else obj.note
    get_note_short.short_description = "Note"
    
    def get_note2_short(self, obj):
        return obj.note2[:20] + "..." if obj.note2 and len(obj.note2) > 20 else obj.note2
    get_note2_short.short_description = "Note 2"
    
    # Pomocné metody pro zobrazení názvů z cizích klíčů
    def get_project_number(self, obj):
        return obj.project_number.name if obj.project_number else "N/A"
    get_project_number.short_description = "Project Number"

    def get_aac_mold_number(self, obj):
        return obj.aac_mold_number.name if obj.aac_mold_number else "N/A"
    get_aac_mold_number.short_description = "AAC Mold Number"
    
    def get_mold_number(self, obj):
        return obj.mold_number.name if obj.mold_number else "N/A"
    get_mold_number.short_description = "Mold Number"

    def get_surface(self, obj):
        return obj.surface.name if obj.surface else "N/A"
    get_surface.short_description = "Surface"

    def get_moldset_preform(self, obj):
        return obj.moldset_preform.name if obj.moldset_preform else "N/A"
    get_moldset_preform.short_description = "Moldset Preform"

    def get_parent_layout(self, obj):
        return obj.parent_layout.name if obj.parent_layout else "N/A"
    get_parent_layout.short_description = "Parent Layout"
    
    def get_machine(self, obj):
        return obj.machine.name if obj.machine else "N/A"
    get_machine.short_description = "Machine"
    
    def get_machining_type(self, obj):
        return obj.machining_type.name if obj.machining_type else "N/A"
    get_machining_type.short_description = "Machining Type"
    
    def get_operator(self, obj):
        return obj.operator.name if obj.operator else "N/A"
    get_operator.short_description = "Operator"
    
    def get_status(self, obj):
        return obj.status.name if obj.status else "N/A"
    get_status.short_description = "Status"
    
    def get_task(self, obj):
        return obj.task.name if obj.task else "N/A"
    get_task.short_description = "Task"