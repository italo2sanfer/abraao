from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Joao, Judite, Paty, Davi, Group
from .utils import encrypt_password


def is_daviown(request):
    davi = Davi.objects.get(user=request.user)
    if davi and davi.role == Davi.ROLE_OWN:
        return True
    return False


class DaviAdmin(admin.ModelAdmin):
    list_display = ["user", "role"]


class WithDaviAdmin(admin.ModelAdmin):
    def get_profile(self, obj):
        return mark_safe(f"<span>{obj.davi.user.username}</span>")

    get_profile.short_description = "user"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if is_daviown(request):
            return qs.filter(davi__user=request.user)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if is_daviown(request):
            if db_field.name == "davi":
                kwargs["queryset"] = Davi.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class JuditeAdmin(WithDaviAdmin):
    list_display = ["get_profile", "code", "passwd", "get_description", "get_ties"]
    ordering = ("code",)
    search_fields = ("code", "description")
    list_filter = ["code"]
    exclude = ("passwd",)

    def get_description(self, obj):
        out = ""
        if obj.description:
            out = "<ul>"
            for part in obj.description.split("<br>"):
                out += f"<li>{part}</li>"
            out += "</ul>"
        return mark_safe("".join(out))

    get_description.short_description = "description"

    def get_ties(self, obj):
        ids_ties = list(
            Joao.objects.filter(access__contains=obj.code).values_list("id", flat=True)
        )
        out = f"<p>{','.join(map(str, ids_ties)) if ids_ties else 'Orphan'}</p>"
        return mark_safe("".join(out))

    get_ties.short_description = "ties"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.passwd = encrypt_password(obj.code, obj.code)
        super().save_model(request, obj, form, change)


class PatyAdmin(WithDaviAdmin):
    list_display = ["get_profile", "name", "url", "get_description", "get_ties"]
    ordering = ("name",)
    search_fields = ("name", "url", "description")
    list_filter = ["name"]

    def get_description(self, obj):
        out = ""
        if obj.description:
            out = "<ul>"
            for part in obj.description.split("<br>"):
                out += f"<li>{part}</li>"
            out += "</ul>"
        return mark_safe("".join(out))

    get_description.short_description = "description"

    def get_ties(self, obj):
        ids_ties = list(obj.joao_set.all().values_list("id", flat=True))
        out = f"<p>{','.join(map(str, ids_ties)) if ids_ties else 'Orphan'}</p>"
        return mark_safe("".join(out))

    get_ties.short_description = "ties"


class JoaoAdmin(WithDaviAdmin):
    list_display = [
        "get_profile",
        "show_actions",
        "get_paty",
        "group",
        "login",
        "get_access",
        "get_description",
    ]
    ordering = ("paty",)
    search_fields = ("paty__name", "paty__url", "group__name", "login", "access", "description")
    list_filter = ["group"]

    def show_actions(self, obj):
        out = (
            f"<a class='success' href='/admin/moises/joao/{obj.id}/change/'>E</a></li>"
        )
        return mark_safe("".join(out))

    show_actions.short_description = "#"

    def get_paty(self, obj):
        paty = obj.paty
        url = (
            ""
            if not paty.url
            else f"<br>URL: <a></a href='{paty.url}' target='_blank'>{paty.url[:28]}...</a>"
        )
        desc = "" if not paty.description else f"<br>Desc: {paty.description[:28]}"
        out = f"{paty.name}{url}{desc}"
        return mark_safe("".join(out))

    get_paty.short_description = "Paty"

    def get_access(self, obj):
        out = "<ul>"
        for part in obj.access.split("<br>"):
            code = part.split(":")
            judite = Judite.objects.filter(code=code[1])
            _id, text = 0, "Not found"
            if judite.exists():
                judite = judite.first()
                _id, text = judite.id, code[0] + ":" + code[1]
            out += f"<li><a href='/admin/moises/judite/{_id}/change/'>E</a>&nbsp;<a href='/moises/judite/{_id}/'>{text}</a></li>"
        out += "</ul>"
        return mark_safe("".join(out))

    get_access.short_description = "access"

    def get_description(self, obj):
        out = ""
        if obj.description:
            out = "<ul>"
            for part in obj.description.split("<br>"):
                out += f"<li>{part}</li>"
            out += "</ul>"
        return mark_safe("".join(out))

    get_description.short_description = "description"


class DaviAdmin(admin.ModelAdmin):
    list_display = ["user", "role"]


class GroupAdmin(WithDaviAdmin):
    list_display = ["get_profile", "name", "description"]


admin.site.register(Judite, JuditeAdmin)
admin.site.register(Paty, PatyAdmin)
admin.site.register(Joao, JoaoAdmin)
admin.site.register(Davi, DaviAdmin)
admin.site.register(Group, GroupAdmin)