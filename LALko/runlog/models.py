# runlog/models.py

from django.db import models

# --- Nový model Project, který chyběl ---
class Project(models.Model):
    project_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    aac_mold_number = models.CharField(max_length=100, null=True, blank=True)
    mold_number = models.CharField(max_length=100, null=True, blank=True)
    surface = models.CharField(max_length=100, null=True, blank=True)
    moldset = models.IntegerField(null=True, blank=True)
    preform = models.IntegerField(null=True, blank=True)
    layout = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.project_number or "Untitled Project"

# --- Stávající modely s opraveným modelem Operator ---

class Machine(models.Model):
    """Machine available for operations (e.g., P400 Máňa, S500U Káťa)."""
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Machine"
        verbose_name_plural = "Machines"
    def __str__(self):
        return self.name

class Operator(models.Model):
    """Operator/Technician performing the operation (e.g., THA, JKL)."""
    # Odstraněn OneToOneField na User, použijeme jen pole 'name'
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Operator"
        verbose_name_plural = "Operators"
    def __str__(self):
        return self.name

class Status(models.Model):
    """Status of a task (On Hold, In Progress, Completed)."""
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
    def __str__(self):
        return self.name

class Task(models.Model):
    """Type of task performed (from Values sheet)."""
    task_name = models.CharField(max_length=100)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
    def __str__(self):
        return f"{self.task_name} ({self.status or 'No status'})"

class MachiningType(models.Model):
    """Machining type of the operation (LineByLine, Spiral, LongPlate)."""
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Machining Type"
        verbose_name_plural = "Machining Types"
    def __str__(self):
        return self.name

class Operation(models.Model):
    """Main log entry for a laser ablation operation."""
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True, blank=True)
    machining_type = models.ForeignKey(MachiningType, on_delete=models.CASCADE, null=True, blank=True)
    # Vztah k operátorům
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)
    
    # Technická data
    x_levelling = models.FloatField(blank=True, null=True)
    y_levelling = models.FloatField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    notes2 = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Operation"
        verbose_name_plural = "Operations"
        
    def __str__(self):
        return f"Operation for {self.project or 'N/A'}"