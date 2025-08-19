from django.db import models
from django.contrib.auth.models import User


class Machine(models.Model):
    """Machine available for operations (e.g., P400 Máňa, S500U Káťa)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Machine"
        verbose_name_plural = "Machines"

    def __str__(self):
        return self.name


class Operator(models.Model):
    """Operator/Technicien performing the operation (e.g., THA, JKL)."""
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Operator"
        verbose_name_plural = "Operators"

    def __str__(self):
        return self.name


class Task(models.Model):
    """Type of task performed (from Values sheet)."""
    task_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"{self.task_name} ({self.status})"


class Project(models.Model):
    """Project details related to an operation."""
    project_number = models.CharField(max_length=50)
    aac_mold_number = models.CharField(max_length=50)
    mold_number = models.CharField(max_length=50)
    surface = models.CharField(max_length=20)
    moldset = models.IntegerField()
    preform = models.IntegerField()
    layout = models.IntegerField()

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return f"{self.project_number} / {self.mold_number}"


class MachiningType(models.Model):
    """Machining type of the operation (LineByLine, Spiral, LongPlate)."""
    MACHINING_CHOICES = [
        ("LineByLine", "LineByLine"),
        ("Spiral", "Spiral"),
        ("LongPlate", "LongPlate"),
    ]
    name = models.CharField(max_length=50, choices=MACHINING_CHOICES, unique=True)

    class Meta:
        verbose_name = "Machining Type"
        verbose_name_plural = "Machining Types"

    def __str__(self):
        return self.name


class Operation(models.Model):
    """Main log entry for a laser ablation operation."""
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    operators = models.ManyToManyField(Operator, related_name="operations")  # změněno z ForeignKey
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    machining_type = models.ForeignKey(MachiningType, on_delete=models.CASCADE)

    x_levelling = models.FloatField()
    y_levelling = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    notes2 = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Operation"
        verbose_name_plural = "Operations"

    def __str__(self):
        return f"{self.task} on {self.machine} ({self.start_time})"
