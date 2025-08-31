# runlog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Operation, Machine, Operator, ChangeLog
from .forms import OperationForm
from .tables import OperationTable
from .filters import OperationFilter
from django.core.paginator import Paginator
import json

def operation_filter(request):
    """Zobrazí formulář pro filtrování."""
    f = OperationFilter(request.GET, queryset=Operation.objects.all())
    
    return render(request, "runlog/operation_filter.html", {
        "filter_form": f.form
    })

def operation_results(request):
    # Data se řadí před odesláním do tabulky
    filter_instance = OperationFilter(request.GET, queryset=Operation.objects.all().order_by('-id'))
    filtered_qs = filter_instance.qs
    
    table = OperationTable(filtered_qs)
    
    table.paginate(page=request.GET.get("page", 1), per_page=0)
    
    return render(request, "runlog/operation_results.html", {
        "table": table,
        "filter_form": filter_instance.form
    })

def operation_list(request):
    """Zobrazí všechny operace (bez filtrování)."""
    # Seřadí QuerySet podle ID (od nejvyššího po nejnižší)
    table = OperationTable(Operation.objects.all().order_by('-id'))
    table.paginate(page=request.GET.get("page", 1), per_page=100)
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
    """
    operation = None
    before_change_data = None
    
    if pk:
        # Získání původních dat PŘED zpracováním formuláře
        operation = get_object_or_404(Operation, pk=pk)
        before_change_data = get_object_data(operation)

    if request.method == 'POST':
        form = OperationForm(request.POST, instance=operation)
        if form.is_valid():
            # Uložíme instanci bez uložení do databáze, abychom mohli získat ID
            new_operation = form.save(commit=False)
            new_operation.save() # Uložíme model
            form.save_m2m() # Uložíme Many-to-many vztahy

            # Získáme data PO uložení
            after_change_data = get_object_data(new_operation)

            if pk:
                action = 'edited'
            else:
                action = 'created'
            
            ChangeLog.objects.create(
                action=action,
                model_name='Operation',
                object_id=new_operation.pk,
                user=request.user if request.user.is_authenticated else None,
                before_change=before_change_data,
                after_change=after_change_data
            )

            return redirect('operation_list')
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
    # Získání všech záznamů a seřazení od nejnovějších
    all_logs = ChangeLog.objects.order_by('-timestamp')

    # Porovnání dat pro zobrazení pouze změn
    for log in all_logs:
        if log.action == 'edited' and log.before_change and log.after_change:
            diffs = {}
            before_items = log.before_change.items()
            after_items = log.after_change.items()
            
            # Najde klíče, které byly změněny
            for key, after_value in after_items:
                # Najde odpovídající hodnotu v datech "před"
                before_value = log.before_change.get(key)
                # Porovná obě hodnoty
                if before_value != after_value:
                    diffs[key] = {
                        'before': before_value,
                        'after': after_value
                    }
            log.diffs = diffs
        else:
            log.diffs = None

    paginator = Paginator(all_logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'runlog/activity_log.html', context)
