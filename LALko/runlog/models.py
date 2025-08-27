from django.db import models
from django.contrib.auth.models import User
#from .models import Operation

class AACMoldNumber(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "AAC Mold Number"
        verbose_name_plural = "AAC Mold Numbers"
        
    def __str__(self):
        return str(self.name) or "N/A"
    
class Machine(models.Model):
    """Machine available for operations (e.g., P400 Máňa, S500U Káťa)."""
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Machine"
        verbose_name_plural = "Machines"
    def __str__(self):
        return str(self.name) or "Unnamed Machine"
    
class MachiningType(models.Model):
    """Machining type of the operation (LineByLine, Spiral, LongPlate)."""
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Machining Type"
        verbose_name_plural = "Machining Types"
    def __str__(self):
        return str(self.name) or "N/A"

class MoldNumber(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Mold Number"
        verbose_name_plural = "Mold Numbers"
        
    def __str__(self):
        return str(self.name) or "N/A"

class MoldsetPreform(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Moldset Preform"
        verbose_name_plural = "Moldset Preforms"
        
    def __str__(self):
        return str(self.name) or "N/A"

class Operator(models.Model):
    """Operator/Technician performing the operation (e.g., THA, JKL)."""
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name = "Operator"
        verbose_name_plural = "Operators"
    def __str__(self):
        return str(self.name)

class ParentLayout(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Parent Layout"
        verbose_name_plural = "Parent Layouts"
        
    def __str__(self):
        return str(self.name) or "N/A"

class ProjectNumber(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Project Number"
        verbose_name_plural = "Project Numbers"
        
    def __str__(self):
        return str(self.name) or "N/A"

class Status(models.Model):
    """Status of a task (On Hold, In Progress, Completed)."""
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
    def __str__(self):
        return str(self.name) or "N/A"

class Surface(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Surface"
        verbose_name_plural = "Surfaces"

    def __str__(self):
        return self.name

class Task(models.Model):
    """Type of task performed (from Values sheet)."""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
    def __str__(self):
        return str(self.name)

class Operation(models.Model):
    """Main log entry for a laser ablation operation."""
    # Data
    aac_mold_number = models.ForeignKey(AACMoldNumber, on_delete=models.SET_NULL, null=True, blank=True)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True, blank=True)
    machining_type = models.ForeignKey(MachiningType, on_delete=models.CASCADE, null=True, blank=True)
    #mold_number = models.ForeignKey(MoldNumber, on_delete=models.SET_NULL, null=True, blank=True)
    mold_number = models.CharField(max_length=10, blank=True, null=True)
    moldset_preform = models.ForeignKey(MoldsetPreform, on_delete=models.SET_NULL, null=True, blank=True)
    #operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    operators = models.ManyToManyField("Operator", blank=True, verbose_name="Operators")
    parent_layout = models.ForeignKey(ParentLayout, on_delete=models.SET_NULL, null=True, blank=True)
    project_number = models.ForeignKey(ProjectNumber, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    surface = models.ForeignKey(Surface, on_delete=models.SET_NULL, null=True, blank=True)    
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    description = models.TextField(blank=True, null=True)

    x_levelling = models.FloatField(blank=True, null=True)
    y_levelling = models.FloatField(blank=True, null=True)
    
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    
    note = models.TextField(blank=True, null=True)
    note2 = models.TextField(blank=True, null=True)
    
    # Přidání metody save()
    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            time_delta = self.end_time - self.start_time
            # Převedení na minuty
            self.duration = time_delta.total_seconds() / 3600
            
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Operation"
        verbose_name_plural = "Operations"
        
    def __str__(self):
        return f"Operation for {self.project_number or 'N/A'}"
    
    # runlog/models.py

class ChangeLog(models.Model):
    ACTION_CHOICES = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
    )
    
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50)
    object_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    before_change = models.JSONField(null=True, blank=True)
    after_change = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} {self.action} {self.model_name} (ID: {self.object_id})"