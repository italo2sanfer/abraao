from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Judite, Paty, Joao


class JuditeAdmin(admin.ModelAdmin):
    list_display = ['code', 'passwd', 'description']
    ordering = ('code',)
    search_fields = ('code', 'description')
    list_filter = ['code']
admin.site.register(Judite, JuditeAdmin)


class PatyAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'get_description']
    ordering = ('name',)
    search_fields = ('name', 'url', 'description')
    list_filter = ['name']

    def get_description(self, obj):
        out = ""
        if obj.description:
            out = f"<ul>"
            for part in obj.description.split('<br>'):
                out += f"<li>{part}</li>"
            out += f"</ul>"
        return mark_safe(''.join(out))
    get_description.short_description = 'description'

admin.site.register(Paty, PatyAdmin)


class JoaoAdmin(admin.ModelAdmin):
    list_display = ['show_actions', 'get_paty', 'who', 'login','get_access', 'get_description']
    ordering = ('paty',)
    search_fields = ('paty__name', 'paty__url', 'who', 'login','access', 'description')
    list_filter = ['who']

    def show_actions(self, obj):
        out = f"<a class='success' href='/admin/passapp/joao/{obj.id}/change/'>E</a></li>"
        return mark_safe(''.join(out))
    show_actions.short_description = '#'

    def get_paty(self, obj):
        paty = obj.paty
        url = "" if not paty.url else f"<br>URL: <a></a href='{paty.url}' target='_blank'>{paty.url[:28]}...</a>"
        desc = "" if not paty.description else f"<br>Desc: {paty.description[:28]}"
        out = f"{paty.name}{url}{desc}"
        return mark_safe(''.join(out))    
    get_paty.short_description = 'Paty'

    def get_access(self, obj):
        out = f"<ul>"
        for part in obj.access.split('<br>'):
            code = part.split(':')
            judite = Judite.objects.filter(code=code[1])
            _id, text = 0, "Not found"
            if judite.exists():
                judite = judite.first()
                _id, text = judite.id, code[0]+":"+code[1]
            out += f"<li><a href='/admin/passapp/judite/{_id}/change/'>E</a>&nbsp;<a href='/passapp/judite/{_id}/'>{text}</a></li>"
        out += f"</ul>"
        return mark_safe(''.join(out))
    get_access.short_description = 'access'

    def get_description(self, obj):
        out = ""
        if obj.description:
            out = f"<ul>"
            for part in obj.description.split('<br>'):
                out += f"<li>{part}</li>"
            out += f"</ul>"
        return mark_safe(''.join(out))
    get_description.short_description = 'description'

admin.site.register(Joao, JoaoAdmin)