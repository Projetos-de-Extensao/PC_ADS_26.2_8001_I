from urllib import response

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError
from catalogo.models import ModuloPortal,Tema,Assunto,ServicoCatalogo
from .models import SolicitacaoZeladoria,HistoricoSolicitacao
from .services import alterar_status
from unittest.mock import patch

User=get_user_model()
class RegrasCriticasTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Monta a cadeia real de catálogo necessária para registrar uma solicitação.
        m=ModuloPortal.objects.create(nome="Zeladoria")
        t=Tema.objects.create(modulo=m,nome="Vias")
        a=Assunto.objects.create(tema=t,nome="Buracos")
        cls.servico=ServicoCatalogo.objects.create(assunto=a,nome="Reparo",descricao="Reparo de buracos")
        cls.cidadao=User.objects.create_user(username="cidadao",email="cidadao@teste.com",password="Senha12345")
        cls.outro=User.objects.create_user(username="outro",email="outro@teste.com",password="Senha12345")
        cls.servidor=User.objects.create_user(username="servidor",email="servidor@teste.com",password="Senha12345",tipo="SERVIDOR")

    def test_criar_solicitacao_cria_historico_inicial(self):
        print("\n[TESTE 1] CRIACAO DE SOLICITACAO E HISTORICO", flush=True)
        print("Cenario: cidadao autenticado registra uma solicitacao.", flush=True)
        # 1) O cidadão autenticado envia os dados do serviço e endereço.
        c=APIClient(); c.force_authenticate(self.cidadao)
        r=c.post("/api/solicitacoes/",{"servico":self.servico.id,"descricao":"Buraco na rua","bairro":"Centro","respostas_adicionais":{"urgencia":"alta"}},format="json")
        # 2) A API deve persistir a solicitação e seu evento CRIACAO na mesma operação.
        self.assertEqual(r.status_code,201,r.data)
        s=SolicitacaoZeladoria.objects.get(pk=r.data["id"])
        self.assertEqual(s.solicitante,self.cidadao)
        self.assertEqual(s.status,SolicitacaoZeladoria.Status.RECEBIDA)
        h=HistoricoSolicitacao.objects.get(solicitacao=s)
        self.assertEqual(h.acao,HistoricoSolicitacao.Acao.CRIACAO)
        self.assertEqual(h.status_novo,SolicitacaoZeladoria.Status.RECEBIDA)
        print(f"Solicitacao criada: ID {s.id}", flush=True)
        print(f"Status inicial: {s.status}", flush=True)
        print(f"Evento registrado: {h.acao}", flush=True)
        print("[APROVADO] Solicitacao e historico persistidos corretamente.", flush=True)

    def test_mudanca_status_audita_e_estado_final_bloqueia_nova_mudanca(self):
        # 1) Cria uma solicitação no estado inicial e avança para análise.
        s=SolicitacaoZeladoria.objects.create(solicitante=self.cidadao,servico=self.servico,descricao="Poste apagado")
        h=alterar_status(s.id,SolicitacaoZeladoria.Status.EM_ANALISE,self.servidor)
        s.refresh_from_db()
        # 2) Confere estado atual e registro dos estados anterior/novo.
        self.assertEqual(s.status,SolicitacaoZeladoria.Status.EM_ANALISE)
        self.assertEqual(h.status_anterior,SolicitacaoZeladoria.Status.RECEBIDA)
        self.assertEqual(h.status_novo,SolicitacaoZeladoria.Status.EM_ANALISE)
        # 3) Conclui e tenta reabrir: regra impede transição após encerramento.
        alterar_status(s.id,SolicitacaoZeladoria.Status.CONCLUIDA,self.servidor)
        n=s.historico.count()
        with self.assertRaises(ValidationError):
            alterar_status(s.id,SolicitacaoZeladoria.Status.EM_ATENDIMENTO,self.servidor)
        self.assertEqual(s.historico.count(),n)

    def test_cidadao_nao_consulta_solicitacao_de_terceiro(self):
        print("\n[TESTE 3] ISOLAMENTO DE SOLICITACOES POR CIDADAO", flush=True)
        print("Cenario: um cidadao tenta consultar solicitacoes de outros usuarios.", flush=True)
        # 1) Registra uma solicitação para cada cidadão.
        SolicitacaoZeladoria.objects.create(solicitante=self.cidadao,servico=self.servico,descricao="Minha rua")
        SolicitacaoZeladoria.objects.create(solicitante=self.outro,servico=self.servico,descricao="Rua de terceiro")
        # 2) Consulta autenticada como o primeiro cidadão.
        c=APIClient(); c.force_authenticate(self.cidadao); r=c.get("/api/solicitacoes/")
        # 3) Apenas o próprio registro deve aparecer, evitando exposição de dados pessoais.
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.data["count"],1)
        self.assertEqual(r.data["results"][0]["descricao"],"Minha rua")
        print(f"Solicitacoes retornadas pela API: {r.data['count']}", flush=True)
        print("Solicitacao de terceiro: nao retornada.", flush=True)
        print("[APROVADO] O cidadao acessou somente seus proprios registros.", flush=True)


    def test_falha_ao_registrar_historico_reverte_criacao(self):
        print("\n[TESTE 2] ROLLBACK DE TRANSACAO", flush=True)
        print("Cenario: falha simulada ao registrar o historico.", flush=True)
        c = APIClient()
        c.force_authenticate(self.cidadao)

        with patch(
            "zeladoria.views.registrar_criacao",
            side_effect=ValidationError(
                "Falha de regra de negócio simulada."
            )
        ):
            response = c.post(
                "/api/solicitacoes/",
                {
                    "servico": self.servico.id,
                    "descricao": "Buraco na rua",
                    "bairro": "Centro",
                },
                format="json",
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(SolicitacaoZeladoria.objects.count(), 0)
        self.assertEqual(HistoricoSolicitacao.objects.count(), 0)
        print(f"Status HTTP recebido: {response.status_code}", flush=True)
        print(f"Solicitacoes restantes: {SolicitacaoZeladoria.objects.count()}", flush=True)
        print(f"Historicos restantes: {HistoricoSolicitacao.objects.count()}", flush=True)
        print("[APROVADO] A transacao foi revertida; nenhum registro parcial permaneceu.", flush=True)