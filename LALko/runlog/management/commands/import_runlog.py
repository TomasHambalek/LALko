# runlog/management/commands/import_runlog.py

from django.core.management.base import BaseCommand
from runlog.models import Operation, Machine, MachiningType, Operator
import pandas as pd
from pathlib import Path

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

        df = pd.read_excel(excel_path, sheet_name="Runlog", engine='openpyxl', skiprows=1)

        try:
            machine = Machine.objects.get(name="P400 Máňa")
            machining_type = MachiningType.objects.get(name="Line By Line")
        except Machine.DoesNotExist:
            self.stderr.write(self.style.ERROR("Chyba: Stroj 'P400 Máňa' nenalezen v DB."))
            return
        except MachiningType.DoesNotExist:
            self.stderr.write(self.style.ERROR("Chyba: Typ obrábění 'Line By Line' nenalezen v DB."))
            return

        count = 0

        for index, row in df.iterrows():
            try:
                op = Operation.objects.create(
                    task=row.get('Task'),
                    description=row.get('Description', ''),
                    status=row.get('Status'),
                    x_levelling=row.get('X Levelling'),
                    y_levelling=row.get('Y Levelling'),
                    project_number=row.get('Project Number'),
                    aac_mold_number=row.get('AAC Mold Number'),
                    mold_number=row.get('Mold Number'),
                    surface=row.get('Surface'),
                    moldset_preform=row.get('Moldset Preform'),
                    parent_layout=row.get('Parent Layout'),
                    start_time=row.get('Start Time'),
                    end_time=row.get('End Time'),
                    duration=row.get('Duration'),
                    note=row.get('Note', ''),
                    note2=row.get('Note2', ''),
                    machine=machine,
                    machining_type=machining_type,
                )

                # Operátoři - rozdělit podle "+" a přiřadit podle `name`
                operators_raw = row.get('Operators')
                if pd.notna(operators_raw):
                    operator_names = [name.strip() for name in str(operators_raw).split('+')]
                    operator_objs = Operator.objects.filter(name__in=operator_names)

                    # Výstraha, pokud některé operátory nenajdeme
                    missing = set(operator_names) - set(operator_objs.values_list('name', flat=True))
                    if missing:
                        self.stderr.write(
                            self.style.WARNING(f"Operátoři nenalezeni: {missing} (řádek {index + 2})")
                        )

                    op.operators.set(operator_objs)

                count += 1

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Chyba při zpracování řádku {index + 2}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Import úspěšně dokončen. Načteno {count} záznamů."))
