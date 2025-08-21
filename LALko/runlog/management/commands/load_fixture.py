import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

class Command(BaseCommand):
    help = "Načte všechny fixtures JSON v runlog/fixtures a nahradí obsah tabulek"

    def handle(self, *args, **options):
        fixtures_dir = "runlog/fixtures"

        if not os.path.exists(fixtures_dir):
            raise CommandError(f"Složka {fixtures_dir} neexistuje.")

        for filename in os.listdir(fixtures_dir):
            if not filename.endswith(".json"):
                continue

            fixture_name = filename[:-5]  # bez .json
            file_path = os.path.join(fixtures_dir, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                raise CommandError(f"Chyba v JSON {file_path}: {e}")

            if not data:
                self.stdout.write(self.style.WARNING(f"{filename} je prázdný, přeskakuji."))
                continue

            # první záznam v souboru určí model (např. "runlog.operator")
            model_label = data[0]["model"]
            try:
                model = apps.get_model(model_label)
            except LookupError:
                self.stdout.write(self.style.WARNING(f"Nenalezen model '{model_label}' pro {filename}, přeskakuji."))
                continue

            # Smazat staré hodnoty
            model.objects.all().delete()

            # Načíst nové
            for entry in data:
                model.objects.create(**entry["fields"])

            self.stdout.write(
                self.style.SUCCESS(f"Načteno {len(data)} záznamů do {model.__name__} z {filename}")
            )
