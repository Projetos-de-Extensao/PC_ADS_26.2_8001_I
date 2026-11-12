from django.contrib import admin
from .models import UnidadeAtendimento,UnidadeServico,SolicitacaoZeladoria,HistoricoSolicitacao,AnexoSolicitacao
class UnidadeServicoInline(admin.TabularInline):
    model=UnidadeServico; extra=1
@admin.register(UnidadeAtendimento)
class UnidadeAdmin(admin.ModelAdmin):
    list_display=("codigo","nome","ativo"); list_filter=("ativo",); inlines=[UnidadeServicoInline]
@admin.register(SolicitacaoZeladoria)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display=("protocolo","solicitante","servico","status","criado_em")
    list_filter=("status","servico","unidade_atual"); search_fields=("protocolo","descricao","solicitante__email")
    readonly_fields=("protocolo","criado_em","atualizado_em")
admin.site.register(HistoricoSolicitacao)
admin.site.register(AnexoSolicitacao)
