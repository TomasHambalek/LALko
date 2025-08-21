# runlog/management/commands/load_input_data.py

import os
import importlib
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db.utils import IntegrityError
from django.conf import settings

class Command(BaseCommand):
    help = "Načte data z Python souborů a doplní chybějící záznamy."

    def handle(self, *args, **options):
        # Správná cesta ke složce s daty
        data_dir = os.path.join(settings.BASE_DIR, 'runlog', 'input_data')

        if not os.path.exists(data_dir):
            raise CommandError(f"Složka {data_dir} neexistuje.")

        for filename in os.listdir(data_dir):
            if not filename.endswith(".py") or filename == "__init__.py":
                continue

            module_name = filename[:-3]
            
            try:
                # Upravíme import tak, aby odpovídal struktuře runlog.input_data
                module = importlib.import_module(f"runlog.input_data.{module_name}")
            except ImportError as e:
                self.stdout.write(self.style.ERROR(f"Chyba při importu modulu {module_name}: {e}"))
                continue

            model_name = module_name
            try:
                model = apps.get_model('runlog', model_name.capitalize())
            except LookupError:
                self.stdout.write(self.style.WARNING(f"Nenalezen model '{model_name.capitalize()}', přeskakuji {filename}."))
                continue

            data_list_name = model_name.upper()
            try:
                data_list = getattr(module, data_list_name)
            except AttributeError:
                self.stdout.write(self.style.WARNING(f"Nenalezena proměnná '{data_list_name}' v {filename}, přeskakuji."))
                continue

            for entry in data_list:
                try:
                    obj, created = model.objects.get_or_create(
                        name=entry['name'],
                        defaults=entry
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Vytvořen nový záznam: {obj.name}"))
                    else:
                        self.stdout.write(self.style.NOTICE(f"Záznam '{obj.name}' už existuje, přeskakuji."))
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f"Chyba integrity u záznamu {entry}: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Neznámá chyba u záznamu {entry}: {e}"))
            
            self.stdout.write(self.style.SUCCESS("---"))