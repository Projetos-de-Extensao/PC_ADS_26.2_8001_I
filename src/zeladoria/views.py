from django.db import transaction
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import *
from .permissions import SolicitacaoPermission,servidor
from .serializers import *
from .services import registrar_criacao,alterar_status,encaminhar

class UnidadeViewSet(viewsets.ModelViewSet):
    queryset=UnidadeAtendimento.objects.all(); serializer_class=UnidadeSerializer
    def get_permissions(self):
        return [] if self.action in ("list","retrieve") else [IsAdminUser()]
    
class SolicitacaoViewSet(viewsets.ModelViewSet):
    permission_classes=[SolicitacaoPermission]
    http_method_names = ["get", "post", "put", "patch", "head", "options"]
    filterset_fields=["status","servico","unidade_atual"]; ordering_fields=["criado_em","atualizado_em","status"]; ordering=["-criado_em"]

    def get_queryset(self):
        q = SolicitacaoZeladoria.objects.select_related(
        "solicitante", "servico", "unidade_atual"
        )

        if not servidor(self.request.user):
            q = q.filter(solicitante=self.request.user)

        urgencia = self.request.query_params.get(
        "respostas_adicionais__urgencia"
        )

        if urgencia is not None:
            q = q.filter(respostas_adicionais__urgencia=urgencia)

        return q
    
    def get_serializer_class(self):
        if self.action == "create":
            return SolicitacaoCreateSerializer
        if self.action in ("update", "partial_update"):
            return SolicitacaoUpdateSerializer
        return SolicitacaoReadSerializer

    @transaction.atomic
    def partial_update(self,request,*args,**kwargs):
        self._servidor()
        obj=self.get_object()
        allowed={"descricao","respostas_adicionais","unidade_atual","responsavel"}
        if not set(request.data.keys()).issubset(allowed):
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Campos permitidos: descricao, respostas_adicionais, unidade_atual e responsavel. Use /status/ para alterar status.")
        serializer=self.get_serializer(obj,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        changed=sorted(request.data.keys())
        serializer.save()
        HistoricoSolicitacao.objects.create(solicitacao=obj,ator=request.user,
            acao=HistoricoSolicitacao.Acao.ALTERACAO_DADOS,comentario="Campos alterados: "+", ".join(changed))
        return Response(SolicitacaoReadSerializer(obj).data)
    
    @transaction.atomic
    def perform_create(self,serializer):
        obj=serializer.save(solicitante=self.request.user); registrar_criacao(obj,self.request.user)

    def _servidor(self):
        if not servidor(self.request.user): raise PermissionDenied("Ação exclusiva de servidor.")

    @action(detail=True,methods=["post"])
    def status(self,request,pk=None):
        self._servidor(); e=alterar_status(pk,request.data.get("status"),request.user,request.data.get("comentario",""))
        return Response(HistoricoSerializer(e).data)
    
    @action(detail=True,methods=["post"])
    def encaminhar(self,request,pk=None):
        self._servidor(); unidade=UnidadeAtendimento.objects.get(pk=request.data.get("unidade_destino"))
        e=encaminhar(pk,unidade,request.user,request.data.get("comentario",""))
        return Response(HistoricoSerializer(e).data)
    
    @action(detail=True,methods=["post"])
    def cancelar(self,request,pk=None):
        obj=self.get_object()
        if obj.solicitante_id!=request.user.id: self._servidor()
        e=alterar_status(pk,SolicitacaoZeladoria.Status.CANCELADA,request.user,request.data.get("comentario",""))
        return Response(HistoricoSerializer(e).data)
    
    @action(detail=True,methods=["get"])
    def historico(self,request,pk=None):
        obj=self.get_object()
        return Response(HistoricoSerializer(obj.historico.select_related("ator"),many=True).data)
    
    @action(detail=True,methods=["get","post"],parser_classes=[MultiPartParser,FormParser])
    def anexos(self,request,pk=None):
        obj=self.get_object()
        if request.method=="GET": return Response(AnexoSerializer(obj.anexos.all(),many=True,context={"request":request}).data)
        s=AnexoSerializer(data={"arquivo":request.FILES.get("arquivo")},context={"request":request})
        s.is_valid(raise_exception=True); s.save(solicitacao=obj)
        return Response(s.data,status=status.HTTP_201_CREATED)
