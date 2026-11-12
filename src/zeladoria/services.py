from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import SolicitacaoZeladoria,HistoricoSolicitacao
@transaction.atomic
def registrar_criacao(obj,ator):
    return HistoricoSolicitacao.objects.create(solicitacao=obj,ator=ator,acao=HistoricoSolicitacao.Acao.CRIACAO,status_novo=obj.status)
@transaction.atomic
def alterar_status(pk,novo,ator,comentario=""):
    obj=SolicitacaoZeladoria.objects.select_for_update().get(pk=pk)
    if novo not in dict(SolicitacaoZeladoria.Status.choices): raise ValidationError({"status":"Status inválido."})
    if obj.status in (obj.Status.CONCLUIDA,obj.Status.CANCELADA): raise ValidationError({"status":"Solicitação encerrada não pode mudar de status."})
    if obj.status==novo: raise ValidationError({"status":"A solicitação já possui esse status."})
    anterior=obj.status; obj.status=novo; obj.save(update_fields=["status","atualizado_em"])
    acao=HistoricoSolicitacao.Acao.ALTERACAO_STATUS
    if novo==obj.Status.CONCLUIDA: acao=HistoricoSolicitacao.Acao.CONCLUSAO
    if novo==obj.Status.CANCELADA: acao=HistoricoSolicitacao.Acao.CANCELAMENTO
    return HistoricoSolicitacao.objects.create(solicitacao=obj,ator=ator,acao=acao,status_anterior=anterior,status_novo=novo,comentario=comentario)
@transaction.atomic
def encaminhar(pk,unidade,ator,comentario=""):
    obj=SolicitacaoZeladoria.objects.select_for_update().get(pk=pk)
    if obj.status in (obj.Status.CONCLUIDA,obj.Status.CANCELADA): raise ValidationError("Solicitação encerrada não pode ser encaminhada.")
    if not unidade.servicos_vinculados.filter(servico=obj.servico,ativo=True).exists():
        raise ValidationError("A unidade não está habilitada para esse serviço.")
    origem=obj.unidade_atual; obj.unidade_atual=unidade; obj.save(update_fields=["unidade_atual","atualizado_em"])
    return HistoricoSolicitacao.objects.create(solicitacao=obj,ator=ator,acao=HistoricoSolicitacao.Acao.ENCAMINHAMENTO,unidade_origem=origem,unidade_destino=unidade,comentario=comentario)
