from django.db import models
from django.contrib.auth.models import User

class Machine(models.Model):
    """Machine available for operations (e.g., P400 Máňa, S500U Káťa)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Operator(models.Model):
    """Operator (technicien), linked to Django User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    """Type of task performed (from Values sheet)."""
    task_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

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

    def __str__(self):
        return self.name


class Operation(models.Model):
    """Main log entry for a laser ablation operation."""
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
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

    def __str__(self):
        return f"{self.task} on {self.machine} ({self.start_time})"
