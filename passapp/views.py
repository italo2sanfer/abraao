from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import csv, io
from django.http import HttpResponse


from .models import Judite, Joao, Paty


@login_required()
def judite(request, judite_id):
    judite = Judite.objects.get(pk=judite_id)
    title = f"Judite {judite.code}"
    return render(request, 'judite.html', locals())


@require_http_methods(["GET", "POST"])
@login_required()
def import_data_model(request):
    title = "Import"
    app_config = apps.get_app_config("passapp")
    models = [
        (m.__name__, getattr(m._meta, "verbose_name", m.__name__).title())
        for m in app_config.get_models()
    ]    
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        if not csv_file:
            messages.error(request, "Nenhum arquivo enviado.")
            return redirect("imp_data")
        try:
            text_io = io.TextIOWrapper(csv_file.file, encoding="utf-8")
            reader = csv.DictReader(text_io)
        except Exception as e:
            messages.error(request, f"Erro ao ler CSV: {e}")
            return redirect("imp_data")

        # Campos permissíveis do modelo (omitindo auto-created, relations)
        model = apps.get_model("passapp", request.POST['model'])
        model_fields = {
            f.name for f in model._meta.get_fields()
            if getattr(f, "editable", True) and not getattr(f, "auto_created", False)
        }

        errors = []
        data = []
        for idx, row in enumerate(reader, start=1):
            # filtra somente colunas que existam no modelo
            data_ = {k: v for k, v in row.items() if k in model_fields and v != ""}
            if not data_:
                errors.append(f"Linha {idx}: nenhuma coluna mapeada para o modelo.")
                continue
            try:
                if model.__name__ == "Joao":
                    data_['paty'] = Paty.objects.filter(name=data_['paty']).first()
                data.append(data_)
            except Exception as e:
                errors.append(f"Line {idx}: {e}")

        if errors:
            for message in errors[:10]:
                messages.error(request, message)
        else:
            for d in data:
                model.objects.create(**d)                
            messages.success(request, f"{len(data)} registros importados.")

        return redirect("imp_data")
    return render(request, "import_data_model.html", locals())


@require_http_methods(["GET", "POST"])
@login_required()
def export_data_model(request):
    """
    Export selected model data as CSV.
    GET: show form with models select.
    POST: return a CSV file with model data.
    """
    title = "Export"
    app_config = apps.get_app_config("passapp")
    models = [
        (m.__name__, getattr(m._meta, "verbose_name", m.__name__).title())
        for m in app_config.get_models()
    ]

    if request.method == "POST":
        model_name = request.POST.get("model")
        if not model_name:
            messages.error(request, "Nenhum modelo selecionado.")
            return redirect("exp_data")

        try:
            model = apps.get_model("passapp", model_name)
        except LookupError:
            messages.error(request, "Modelo não encontrado.")
            return redirect("exp_data")

        # Campos permissíveis do modelo (omitindo auto-created, relations)
        model_fields = [
            f.name for f in model._meta.get_fields()
            if getattr(f, "editable", True) and not getattr(f, "auto_created", False)
        ]
        # Prepare response
        filename = f"{model.__name__}.csv"
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        # Write header
        writer.writerow(model_fields)

        # Write rows
        for obj in model.objects.all():
            row = []
            for field in model_fields:
                try:
                    val = getattr(obj, field)
                    # For related objects, use their string representation
                    if hasattr(val, "__str__") and not isinstance(val, (str, bytes, int, float, type(None))):
                        val = str(val)
                except Exception:
                    val = ""
                row.append(val)
            writer.writerow(row)

        return response

    return render(request, "export_data_model.html", locals())