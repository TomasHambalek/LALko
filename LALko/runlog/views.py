from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Operation, Machine, Operator, ChangeLog
from .forms import OperationForm
from .tables import OperationTable
from .filters import OperationFilter


def operation_filter(request):
    """Zobrazí formulář pro filtrování."""
    f = OperationFilter(request.GET, queryset=Operation.objects.all())
    
    return render(request, "runlog/operation_filter.html", {
        "filter_form": f.form  # Zde je oprava
    })

def operation_results(request):
    filter_form = OperationFilter(request.GET, queryset=Operation.objects.all())
    filtered_qs = filter_form.qs
    table = OperationTable(filtered_qs)
    
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    
    return render(request, "runlog/operation_results.html", {
        "table": table,
        "filter_form": filter_form
    })

def operation_list(request):
    """Zobrazí všechny operace (bez filtrování)."""
    table = OperationTable(Operation.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    return render(request, "runlog/operation_list.html", {"table": table})
def operation_detail(request, pk):
    """Detail of a single operation."""
    operation = get_object_or_404(Operation, pk=pk)
    return render(request, "runlog/operation_detail.html", {"operation": operation})

# Funkce pro bezpečné získání dat pro JSONField
def get_object_data(obj):
    data = {}
    for field in obj._meta.get_fields():
        field_name = field.name
        # ManyToMany pole se načítají jinak
        if isinstance(field, models.ManyToManyField):
            data[field_name] = [
                {'id': rel_obj.pk, 'name': str(rel_obj)}
                for rel_obj in getattr(obj, field_name).all()
            ]
        # ForeignKeys
        elif isinstance(field, models.ForeignKey):
            field_value = getattr(obj, field_name)
            if field_value:
                data[field_name] = {
                    'id': field_value.pk,
                    'name': str(field_value)
                }
            else:
                data[field_name] = None
        # Ostatní pole
        else:
            data[field_name] = str(getattr(obj, field_name))
    return data

# --- Vaše pohledy ---

def manage_operation(request, pk=None):
    """
    Spravuje přidávání a úpravu operací pomocí jedné funkce.
    Pokud pk není zadané, přidává se nová operace.
    Pokud je pk zadané, upravuje se existující operace.
    """
    operation = None
    if pk:
        operation = get_object_or_404(Operation, pk=pk)

    if request.method == 'POST':
        form = OperationForm(request.POST, instance=operation)
        if form.is_valid():
            form.save()
            return redirect('operation_list') # Přesměrování na seznam operací
    else:
        form = OperationForm(instance=operation)
    
    return render(request, 'runlog/operation_form.html', {'form': form})
def delete_operation(request, pk):
    """Smazání operace s logováním."""
    operation = get_object_or_404(Operation, pk=pk)

    if request.method == 'POST':
        # Uložíme si data PŘED smazáním
        before_change_data = get_object_data(operation)

        ChangeLog.objects.create(
            action='deleted',
            model_name='Operation',
            object_id=operation.pk,
            user=request.user if request.user.is_authenticated else None,
            before_change=before_change_data,
            after_change=None
        )

        operation.delete()
        return redirect('operation_list')
        
    return render(request, 'runlog/operation_confirm_delete.html', {'operation': operation})

@login_required
def activity_log(request):
    logs = ChangeLog.objects.order_by('-timestamp')[:50] # Zobrazí posledních 50 záznamů
    context = {
        'logs': logs,
    }
    return render(request, 'runlog/activity_log.html', context)
