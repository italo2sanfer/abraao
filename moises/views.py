from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import csv, io
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.db.models import Q

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
    app_config = apps.get_app_config("moises")
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
        model = apps.get_model("moises", request.POST['model'])
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
    app_config = apps.get_app_config("moises")
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
            model = apps.get_model("moises", model_name)
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


@require_http_methods(["GET"])
def _check_api_token(request):
    auth = request.META.get("HTTP_AUTHORIZATION", "")
    if auth.startswith("Token "):
        token = auth.split(" ", 1)[1]
        print(f"Received token: {token}, Token in settings: {getattr(settings, 'PASSAPP_API_TOKEN', None)}")
        if getattr(settings, "PASSAPP_API_TOKEN", None) and token == settings.PASSAPP_API_TOKEN:
            return True
    return False

@require_http_methods(["GET", "OPTIONS"])
def api_search_joao(request):
    """
    API autenticada (Token) para buscar registros de Joao.
    Query param: ?q=<valor>
    Pesquisa em: paty__name, paty__url, who, login, access, description
    Retorna lista JSON com dados de Joao + paty. No campo `access` cada código
    recebe a senha clara do Judite (campo passwd) entre parênteses logo após o código.
    Autenticação: header HTTP Authorization: Token <PASSAPP_API_TOKEN>
    """
    # Responde preflight sem exigir autenticação
    if request.method == "OPTIONS":
        resp = HttpResponse()
        resp["Allow"] = "GET, OPTIONS"
        return resp

    if not _check_api_token(request):
        return JsonResponse({"detail": "Authentication credentials were not provided or invalid."}, status=401)

    q = (request.GET.get("q") or "").strip()
    if not q:
        return JsonResponse({"detail": "Parâmetro 'q' é obrigatório."}, status=400)

    qs = Joao.objects.select_related("paty").filter(
        Q(paty__name__icontains=q)
        | Q(paty__url__icontains=q)
        | Q(who__icontains=q)
        | Q(login__icontains=q)
        | Q(access__icontains=q)
        | Q(description__icontains=q)
    )

    results = []
    for obj in qs:
        # monta paty
        paty = None
        if obj.paty:
            paty = {
                "id": obj.paty.id,
                "name": obj.paty.name,
                "url": obj.paty.url,
                "description": obj.paty.description,
            }

        # processa access: cada parte separada por '<br>' (conforme uso no projeto)
        parts = [p for p in (obj.access or "").split("<br>") if p != ""]
        new_parts = []
        for part in parts:
            if ":" in part:
                label, code = part.split(":", 1)
                jud = Judite.objects.filter(code=code).first()
                passwd = jud.passwd if jud else ""
                if passwd:
                    new_parts.append(f"{label}:{code}({passwd})")
                else:
                    new_parts.append(f"{label}:{code}")
            else:
                new_parts.append(part)
        access_with_pw = "<br>".join(new_parts)

        results.append({
            "id": obj.id,
            "paty": paty,
            "who": obj.who,
            "login": obj.login,
            "access": access_with_pw,
            "description": obj.description,
        })

    return JsonResponse(results, safe=False)