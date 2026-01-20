
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.db.models import Q
from django.views.decorators.http import require_GET
from moises.models import Judite, Joao

@require_http_methods(["GET"])
def _check_token(request):
    auth = request.META.get("HTTP_AUTHORIZATION", "")
    if auth.startswith("Token "):
        token = auth.split(" ", 1)[1]
        if getattr(settings, "PASSAPP_API_TOKEN", None) and token == settings.PASSAPP_API_TOKEN:
            return True
    return False

@require_http_methods(["GET", "OPTIONS"])
def joao_search(request):
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

    if not _check_token(request):
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

@require_GET
def judite_passwd(request, code):
    """
    GET /.../judite/<code>/passwd/  -> {"code": "<code>", "passwd": "<passwd>"}
    """
    if not _check_token(request):
        return JsonResponse({"detail": "Authentication credentials were not provided or invalid."}, status=401)

    obj = get_object_or_404(Judite, code=code)
    return JsonResponse({"code": obj.code, "passwd": obj.passwd})