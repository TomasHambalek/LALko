from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Operation, Machine
from .forms import OperationForm

def operation_list(request):
    """List all operations."""
    operations = Operation.objects.all()
    return render(request, "runlog/operation_list.html", {"operations": operations})

def operation_detail(request, pk):
    """Detail of a single operation."""
    operation = get_object_or_404(Operation, pk=pk)
    return render(request, "runlog/operation_detail.html", {"operation": operation})

@login_required
def my_operations(request):
    """List operations for logged-in user only."""
    operations = Operation.objects.filter(operator__user=request.user)
    return render(request, "runlog/my_operations.html", {"operations": operations})

@login_required
def add_operation(request):
    """Add new operation via form."""
    if request.method == "POST":
        form = OperationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("operation_list")
    else:
        form = OperationForm()
    return render(request, "runlog/operation_form.html", {"form": form})

def machine_list(request):
    """List all machines."""
    machines = Machine.objects.all()
    return render(request, "runlog/machine_list.html", {"machines": machines})
