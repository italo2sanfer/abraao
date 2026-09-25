import csv
import io

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .models import Davi, Group, Judite, Paty
from .utils import decrypt_password

html_content_403 = """
    <h1>Erro 403: Acesso Proibido</h1>
    <p>Você não tem permissão para acessar esta página.</p>
    <a href="/" style="padding: 10px; background: blue; color: white; text-decoration: none;">Voltar para a Home</a>
"""


def validate_davi(request):
    davi = Davi.objects.get(user=request.user)
    if not davi:
        return False
    else:
        if davi.role != Davi.ROLE_OWN:
            return False
    return True


@login_required()
def judite(request, judite_id):
    judite = Judite.objects.get(pk=judite_id)
    password = decrypt_password(judite.code, judite.passwd)
    title = f"Judite {judite.code}"
    return render(request, "judite.html", locals())


@require_http_methods(["GET", "POST"])
@login_required()
def import_data_model(request):
    if not validate_davi(request):
        return HttpResponseForbidden(html_content_403)

    title = "Import"
    app_config = apps.get_app_config("moises")
    models = [
        (m.__name__, getattr(m._meta, "verbose_name", m.__name__).title())
        for m in app_config.get_models()
        if m.__name__ not in ["Davi", "Group"]
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
        model = apps.get_model("moises", request.POST["model"])
        model_fields = {
            f.name
            for f in model._meta.get_fields()
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
                davi_str = data_["davi"].split(" ")
                if davi_str[0] == request.user.username:
                    data_["davi"] = Davi.objects.filter(
                        user__username=davi_str[0]
                    ).first()
                    if model.__name__ == "Joao":
                        data_["paty"] = Paty.objects.filter(
                            davi__user=request.user, name=data_["paty"]
                        ).first()
                        group, created = Group.objects.get_or_create(
                            davi=Davi.objects.get(user=request.user),
                            name=data_["group"],
                            defaults={"description": " "},
                        )
                        data_["group"] = group
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

    if not validate_davi(request):
        return HttpResponseForbidden(html_content_403)

    title = "Export"
    app_config = apps.get_app_config("moises")
    models = [
        (m.__name__, getattr(m._meta, "verbose_name", m.__name__).title())
        for m in app_config.get_models()
        if m.__name__ not in ["Davi", "Group"]
    ]

    if request.method == "POST":
        model_name = request.POST.get("model")
        if not model_name:
            messages.error(request, "Nenhum modelo selecionado.")
            return redirect("exp_data")

        try:
            model = apps.get_model("moises", model_name)
        except LookupError:
            messages.error(request, "Modelo não encontrado.")
            return redirect("exp_data")

        # Campos permissíveis do modelo (omitindo auto-created, relations)
        model_fields = [
            f.name
            for f in model._meta.get_fields()
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
            if obj.davi.user == request.user:
                row = []
                for field in model_fields:
                    try:
                        val = getattr(obj, field)
                        # For related objects, use their string representation
                        if hasattr(val, "__str__") and not isinstance(
                            val, (str, bytes, int, float, type(None))
                        ):
                            val = str(val)
                    except Exception:
                        val = ""
                    row.append(val)
                writer.writerow(row)

        return response

    return render(request, "export_data_model.html", locals())


@require_GET
def judite_passwd(request, code):
    """
    GET /.../judite/<code>/passwd/  -> {"code": "<code>", "passwd": "<passwd>"}
    """
    obj = get_object_or_404(Judite, code=code)
    return JsonResponse({"code": obj.code, "passwd": obj.passwd})
