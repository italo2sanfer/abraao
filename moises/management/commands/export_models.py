import csv
import os

from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Exporta todos os modelos do app 'moises' em CSV e JSON. Arquivos em <BASE_DIR>/data."

    def handle(self, *args, **options):
        now = timezone.now().strftime("%Y%m%d_%H%M%S")
        base_dir = getattr(settings, "BASE_DIR", os.getcwd())
        out_dir = os.path.join(base_dir, "data")
        os.makedirs(out_dir, exist_ok=True)

        app_config = apps.get_app_config("moises")
        for model in app_config.get_models():
            model_name = model.__name__
            qs = model.objects.all()

            # JSON (similar to `dumpdata moises.Model`)
            json_fname = f"{model_name}_{now}.json"
            json_path = os.path.join(out_dir, json_fname)
            with open(json_path, "w", encoding="utf-8") as jf:
                jf.write(serializers.serialize("json", qs, indent=2))
            self.stdout.write(f"Wrote JSON: {json_path}")

            # CSV
            csv_fname = f"{model_name}_{now}.csv"
            csv_path = os.path.join(out_dir, csv_fname)
            field_objs = [
                f for f in model._meta.get_fields() if f.concrete and not f.many_to_many
            ]
            headers = [f.name for f in field_objs]

            with open(csv_path, "w", newline="", encoding="utf-8") as cf:
                writer = csv.writer(cf)
                writer.writerow(headers)
                for obj in qs:
                    row = []
                    for f in field_objs:
                        # for FK fields use <field>_id, otherwise the field value
                        if getattr(f, "many_to_one", False):
                            val = getattr(obj, f"{f.name}_id")
                        else:
                            val = getattr(obj, f.name)
                        row.append("" if val is None else str(val))
                    writer.writerow(row)

            self.stdout.write(f"Wrote CSV: {csv_path}")
