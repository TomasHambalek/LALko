from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Operation, Machine, Operator # Přidání modelu Operator
from .forms import OperationForm
from .tables import OperationTable
from .filters import OperationFilter

def operation_filter(request):
    """View for the filter form page."""
    f = OperationFilter(request.GET, queryset=Operation.objects.all())
    return render(request, "runlog/operation_filter.html", {
        "filter": f
    })

def operation_list(request):
    """View for the table with filtered results."""
    f = OperationFilter(request.GET, queryset=Operation.objects.all())
    table = OperationTable(f.qs)

    table.paginate(page=request.GET.get("page", 1), per_page=10)

    return render(request, "runlog/operation_list.html", {
        "table": table,
        "filter": f
    })

def operation_detail(request, pk):
    """Detail of a single operation."""
    operation = get_object_or_404(Operation, pk=pk)
    return render(request, "runlog/operation_detail.html", {"operation": operation})

@login_required
def my_operations(request):
    """List operations for logged-in user only."""
    # Zde je potřeba se ujistit, že model Operator má ForeignKey na User,
    # aby filtr fungoval správně. Pokud ho nemá, musíte ho přidat.
    operations = Operation.objects.filter(operator__user=request.user)
    return render(request, "runlog/my_operations.html", {"operations": operations})

@login_required
def add_operation(request):
    """Add new operation via form."""
    if request.method == "POST":
        form = OperationForm(request.POST)
        if form.is_valid():
            # form.save() automaticky uloží data i z ForeignKey polí
            form.save()
            return redirect("operation_list")
    else:
        form = OperationForm()
    return render(request, "runlog/operation_form.html", {"form": form})

def edit_operation(request, pk):
    operation = get_object_or_404(Operation, pk=pk)
    if request.method == 'POST':
        form = OperationForm(request.POST, instance=operation)
        if form.is_valid():
            # form.save() vypočítá duration, jak jste nastavil v modelu
            form.save()
            return redirect('operation_detail', pk=operation.id)
    else:
        form = OperationForm(instance=operation)
    return render(request, 'runlog/edit_operation.html', {'form': form, 'operation': operation})

def delete_operation(request, pk):
    operation = get_object_or_404(Operation, pk=pk)
    if request.method == 'POST':
        operation.delete()
        return redirect('operation_list')
    return render(request, 'runlog/operation_confirm_delete.html', {'operation': operation}) 