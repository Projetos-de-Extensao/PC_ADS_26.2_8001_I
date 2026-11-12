from django.contrib import admin
from .models import ModuloPortal,Tema,Assunto,ServicoCatalogo
admin.site.register(ModuloPortal)
admin.site.register(Tema)
admin.site.register(Assunto)
@admin.register(ServicoCatalogo)
class ServicoAdmin(admin.ModelAdmin):
    list_display=("codigo","nome","assunto","ativo","prazo_estimado_dias")
    list_filter=("ativo","assunto"); search_fields=("codigo","nome","descricao")
