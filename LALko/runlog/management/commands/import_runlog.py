# runlog/management/commands/import_runlog.py

from django.core.management.base import BaseCommand
from runlog.models import Operation, Machine, MachiningType, Operator, Task, ProjectNumber, AACMoldNumber, MoldsetPreform, Surface, ParentLayout, Status
from django.utils import timezone  # Nový import
import pandas as pd
from pathlib import Path
import re

class Command(BaseCommand):
    help = "Importuje data z Excelu do databáze (Runlog)"

    def add_arguments(self, parser):
        parser.add_argument(
            'excel_path',
            type=str,
            help="Cesta k Excel souboru (.xlsm), např. /home/tomas/LALko/LALko/fixtures/excel_import/runlog.xlsm"
        )

    def handle(self, *args, **options):
        excel_path = Path(options['excel_path'])

        if not excel_path.exists():
            self.stderr.write(self.style.ERROR(f"Soubor {excel_path} neexistuje"))
            return

        df = pd.read_excel(excel_path, sheet_name="Runlog", engine='openpyxl', skiprows=1, header=None)

        df.columns = [
            "Task", "Description", "Status", "X Levelling", "Y Levelling",
            "Project Number", "AAC Mold Number", "Mold Number", "Surface",
            "Moldset Preform", "Parent Layout", "Start Time", "End Time",
            "Duration", "Operators", "Note", "Note2"
        ]

        try:
            machine, _ = Machine.objects.get_or_create(name="P400 Máňa")
            machining_type, _ = MachiningType.objects.get_or_create(name="Line By Line")
            status_obj, _ = Status.objects.get_or_create(name="Completed")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Chyba při inicializaci: {e}"))
            return

        count = 0

        for index, row in df.iterrows():
            try:
                task_value = row['Task']
                if not pd.notna(task_value):
                    self.stderr.write(
                        self.style.WARNING(f"Varování: Přeskočen řádek {index + 2} - chybí povinné pole 'Task'.")
                    )
                    continue

                # Ošetření cizích klíčů (ForeignKey)
                task_obj, _ = Task.objects.get_or_create(name=task_value)
                
                project_number_obj = None
                if pd.notna(row['Project Number']):
                    project_number_obj, _ = ProjectNumber.objects.get_or_create(name=row['Project Number'])

                aac_mold_number_obj = None
                if pd.notna(row['AAC Mold Number']):
                    aac_mold_number_obj, _ = AACMoldNumber.objects.get_or_create(name=row['AAC Mold Number'])

                surface_obj = None
                if pd.notna(row['Surface']):
                    surface_obj, _ = Surface.objects.get_or_create(name=row['Surface'])

                moldset_preform_obj = None
                if pd.notna(row['Moldset Preform']):
                    moldset_preform_obj, _ = MoldsetPreform.objects.get_or_create(name=row['Moldset Preform'])
                
                parent_layout_obj = None
                if pd.notna(row['Parent Layout']):
                    parent_layout_obj, _ = ParentLayout.objects.get_or_create(name=row['Parent Layout'])
                
                # Nová úprava pro ošetření časových zón
                start_time = timezone.make_aware(row['Start Time']) if pd.notna(row['Start Time']) else None
                end_time = timezone.make_aware(row['End Time']) if pd.notna(row['End Time']) else None

                # Vytvoření záznamu s ošetřením prázdných hodnot (NaN)
                op = Operation.objects.create(
                    task=task_obj,
                    description=str(row['Description']) if pd.notna(row['Description']) else '',
                    status=status_obj,
                    x_levelling=row['X Levelling'] if pd.notna(row['X Levelling']) else None,
                    y_levelling=row['Y Levelling'] if pd.notna(row['Y Levelling']) else None,
                    project_number=project_number_obj,
                    aac_mold_number=aac_mold_number_obj,
                    mold_number=str(row['Mold Number']) if pd.notna(row['Mold Number']) else '',
                    surface=surface_obj,
                    moldset_preform=moldset_preform_obj,
                    parent_layout=parent_layout_obj,
                    start_time=start_time,
                    end_time=end_time,
                    duration=row['Duration'] if pd.notna(row['Duration']) else None,
                    note=str(row['Note']) if pd.notna(row['Note']) else '',
                    note2=str(row['Note2']) if pd.notna(row['Note2']) else '',
                    machine=machine,
                    machining_type=machining_type,
                )

                operators_raw = row['Operators']
                if pd.notna(operators_raw):
                    operator_names = [name.strip() for name in str(operators_raw).split('+')]
                    for name in operator_names:
                        operator_obj, _ = Operator.objects.get_or_create(name=name)
                    op.operators.set(Operator.objects.filter(name__in=operator_names))

                count += 1

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Chyba při zpracování řádku {index + 2}: {e}"))
                self.stderr.write(self.style.ERROR(f"Data řádku: {row.to_dict()}"))

        self.stdout.write(self.style.SUCCESS(f"Import úspěšně dokončen. Načteno {count} záznamů."))