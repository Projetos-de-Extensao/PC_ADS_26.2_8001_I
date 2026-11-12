from datetime import timedelta
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from catalogo.models import ServicoCatalogo
from zeladoria.models import (
    AnexoSolicitacao,
    HistoricoSolicitacao,
    SolicitacaoZeladoria,
    UnidadeServico,
)


DEMO_CIDADAOS = [
    {
        "username": "demo.cidadao01",
        "email": "cidadao01@exemplo.com",
        "first_name": "Mariana",
        "last_name": "Oliveira",
        "cpf": "00000000001",
    },
    {
        "username": "demo.cidadao02",
        "email": "cidadao02@exemplo.com",
        "first_name": "Rafael",
        "last_name": "Santos",
        "cpf": "00000000002",
    },
    {
        "username": "demo.cidadao03",
        "email": "cidadao03@exemplo.com",
        "first_name": "Camila",
        "last_name": "Ferreira",
        "cpf": "00000000003",
    },
    {
        "username": "demo.cidadao04",
        "email": "cidadao04@exemplo.com",
        "first_name": "Lucas",
        "last_name": "Costa",
        "cpf": "00000000004",
    },
    {
        "username": "demo.cidadao05",
        "email": "cidadao05@exemplo.com",
        "first_name": "Beatriz",
        "last_name": "Almeida",
        "cpf": "00000000005",
    },
]

DEMO_SERVIDORES = [
    {
        "username": "demo.servidor01",
        "email": "servidor01@exemplo.com",
        "first_name": "André",
        "last_name": "Martins",
        "cpf": "00000000011",
    },
    {
        "username": "demo.servidor02",
        "email": "servidor02@exemplo.com",
        "first_name": "Patrícia",
        "last_name": "Ribeiro",
        "cpf": "00000000012",
    },
]

ENDERECOS = [
    ("Rua da Assembleia", "120", "Centro", "20011000", -22.9035, -43.1777),
    ("Rua Conde de Bonfim", "450", "Tijuca", "20520054", -22.9249, -43.2334),
    ("Avenida Nossa Senhora de Copacabana", "780", "Copacabana", "22060002", -22.9721, -43.1868),
    ("Rua Dias da Cruz", "310", "Méier", "20720010", -22.9025, -43.2802),
    ("Rua Voluntários da Pátria", "210", "Botafogo", "22270010", -22.9514, -43.1860),
    ("Estrada do Portela", "95", "Madureira", "21351050", -22.8718, -43.3396),
    ("Avenida Cesário de Melo", "1500", "Campo Grande", "23050002", -22.9068, -43.5594),
    ("Estrada de Jacarepaguá", "2200", "Jacarepaguá", "22753033", -22.9635, -43.3483),
    ("Rua Santa Clara", "55", "Copacabana", "22041012", -22.9660, -43.1855),
    ("Rua Haddock Lobo", "600", "Tijuca", "20260142", -22.9224, -43.2187),
    ("Rua do Catete", "180", "Catete", "22220000", -22.9260, -43.1788),
    ("Avenida Brasil", "12000", "Penha", "21012000", -22.8240, -43.2900),
]

# As transições são usadas apenas para montar o histórico demonstrativo.
# O status final de cada solicitação já é gravado no próprio registro.
SOLICITACOES_DEMO = [
    {"codigo": "SOL-DEMO-001", "status": "RECEBIDA", "dias": 2, "urgencia": "alta"},
    {"codigo": "SOL-DEMO-002", "status": "EM_ANALISE", "dias": 6, "urgencia": "media"},
    {"codigo": "SOL-DEMO-003", "status": "EM_ATENDIMENTO", "dias": 9, "urgencia": "alta"},
    {"codigo": "SOL-DEMO-004", "status": "PENDENTE", "dias": 12, "urgencia": "baixa"},
    {"codigo": "SOL-DEMO-005", "status": "CONCLUIDA", "dias": 18, "urgencia": "media"},
    {"codigo": "SOL-DEMO-006", "status": "CANCELADA", "dias": 4, "urgencia": "baixa"},
    {"codigo": "SOL-DEMO-007", "status": "RECEBIDA", "dias": 3, "urgencia": "media"},
    {"codigo": "SOL-DEMO-008", "status": "EM_ANALISE", "dias": 7, "urgencia": "alta"},
    {"codigo": "SOL-DEMO-009", "status": "EM_ATENDIMENTO", "dias": 11, "urgencia": "media"},
    {"codigo": "SOL-DEMO-010", "status": "CONCLUIDA", "dias": 24, "urgencia": "baixa"},
    {"codigo": "SOL-DEMO-011", "status": "PENDENTE", "dias": 8, "urgencia": "alta"},
    {"codigo": "SOL-DEMO-012", "status": "CONCLUIDA", "dias": 30, "urgencia": "media"},
]

TRANSICOES = {
    "RECEBIDA": [],
    "EM_ANALISE": ["EM_ANALISE"],
    "EM_ATENDIMENTO": ["EM_ANALISE", "EM_ATENDIMENTO"],
    "PENDENTE": ["EM_ANALISE", "PENDENTE"],
    "CONCLUIDA": ["EM_ANALISE", "EM_ATENDIMENTO", "CONCLUIDA"],
    "CANCELADA": ["CANCELADA"],
}

COMENTARIOS_STATUS = {
    "EM_ANALISE": "Solicitação encaminhada para análise da equipe responsável.",
    "EM_ATENDIMENTO": "Equipe responsável iniciou o atendimento no local.",
    "PENDENTE": "Atendimento aguardando providência ou informação complementar.",
    "CONCLUIDA": "Serviço executado e solicitação concluída.",
    "CANCELADA": "Solicitação cancelada para fins de demonstração.",
}


# Cada solicitação demonstrativa recebe uma imagem sintética correspondente.
# Os arquivos devem ficar na pasta "seed_images" ao lado deste comando.
IMAGENS_DEMO = [
    "01_buraco_na_via.jpg",
    "02_iluminacao_apagada.jpg",
    "03_acumulo_de_lixo.jpg",
    "04_bueiro_obstruido.jpg",
    "05_galho_caido.jpg",
    "06_calcada_danificada.jpg",
    "07_agua_parada.jpg",
    "08_placa_danificada.jpg",
    "09_ponto_de_onibus_vandalizado.jpg",
    "10_parquinho_danificado.jpg",
    "11_banco_quebrado.jpg",
    "12_muro_danificado.jpg",
]


class Command(BaseCommand):
    help = "Cria solicitações demonstrativas, históricos e imagens fictícias como anexos, sem duplicar registros."

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()

        servicos = list(
            ServicoCatalogo.objects.filter(ativo=True)
            .select_related("assunto__tema__modulo")
            .order_by("id")
        )
        if not servicos:
            raise CommandError(
                "Nenhum serviço ativo encontrado. Execute primeiro: "
                "python manage.py seed_catalogo"
            )

        cidadaos = [self._get_or_create_user(User, data, "CIDADAO") for data in DEMO_CIDADAOS]
        servidores = [self._get_or_create_user(User, data, "SERVIDOR") for data in DEMO_SERVIDORES]

        criadas = 0
        existentes = 0
        historicos_criados = 0
        anexos_criados = 0
        agora = timezone.now()
        pasta_imagens = Path(__file__).resolve().parent / "seed_images"

        for indice, dados in enumerate(SOLICITACOES_DEMO):
            servico = servicos[(indice * 2) % len(servicos)]
            cidadao = cidadaos[indice % len(cidadaos)]
            servidor = servidores[indice % len(servidores)]
            endereco = ENDERECOS[indice % len(ENDERECOS)]
            unidade_link = (
                UnidadeServico.objects.filter(
                    servico=servico,
                    ativo=True,
                    unidade__ativo=True,
                )
                .select_related("unidade")
                .order_by("unidade_id")
                .first()
            )
            unidade = unidade_link.unidade if unidade_link else None

            status_final = dados["status"]
            responsavel = None if status_final == "RECEBIDA" else servidor
            protocolo = uuid5(NAMESPACE_URL, f"portal-cidadao-seguro:{dados['codigo']}")
            logradouro, numero, bairro, cep, latitude, longitude = endereco
            criada_em = agora - timedelta(days=dados["dias"])

            solicitacao, foi_criada = SolicitacaoZeladoria.objects.get_or_create(
                protocolo=protocolo,
                defaults={
                    "solicitante": cidadao,
                    "responsavel": responsavel,
                    "servico": servico,
                    "unidade_atual": unidade,
                    "descricao": (
                        f"Solicitação demonstrativa referente ao serviço "
                        f"'{servico.nome}'. Foi identificado um problema no local informado. "
                        "Solicitamos vistoria e providências da equipe responsável."
                    ),
                    "respostas_adicionais": {
                        "origem": "seed_solicitacoes",
                        "codigo_seed": dados["codigo"],
                        "urgencia": dados["urgencia"],
                        "tipo_local": "via_publica",
                        "observacao": "Registro fictício para demonstração acadêmica.",
                    },
                    "formulario_versao": servico.versao_formulario,
                    "status": status_final,
                    "logradouro": logradouro,
                    "numero": numero,
                    "bairro": bairro,
                    "cep": cep,
                    "ponto_referencia": "Localização aproximada para demonstração.",
                    "latitude": latitude,
                    "longitude": longitude,
                },
            )

            if not foi_criada:
                existentes += 1
                if not solicitacao.historico.exists():
                    historicos_criados += self._criar_historico(
                        solicitacao, cidadao, servidor, unidade, status_final, criada_em
                    )
                anexos_criados += self._criar_anexo(
                    solicitacao, cidadao, indice, pasta_imagens
                )
                continue

            criadas += 1
            SolicitacaoZeladoria.objects.filter(pk=solicitacao.pk).update(
                criado_em=criada_em,
                atualizado_em=criada_em,
            )
            historicos_criados += self._criar_historico(
                solicitacao, cidadao, servidor, unidade, status_final, criada_em
            )
            anexos_criados += self._criar_anexo(
                solicitacao, cidadao, indice, pasta_imagens
            )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Seed de solicitações concluído."))
        self.stdout.write(f"Solicitações criadas nesta execução: {criadas}")
        self.stdout.write(f"Solicitações já existentes: {existentes}")
        self.stdout.write(f"Eventos de histórico criados: {historicos_criados}")
        self.stdout.write(f"Anexos criados nesta execução: {anexos_criados}")
        self.stdout.write(f"Total de solicitações no banco: {SolicitacaoZeladoria.objects.count()}")
        self.stdout.write(f"Total de anexos no banco: {AnexoSolicitacao.objects.count()}")
        self.stdout.write(self.style.WARNING("As imagens anexadas são sintéticas e servem apenas para demonstração acadêmica."))

    def _criar_anexo(self, solicitacao, cidadao, indice, pasta_imagens):
        # Evita duplicar anexos quando o comando é executado novamente.
        if solicitacao.anexos.exists():
            return 0

        nome_arquivo = IMAGENS_DEMO[indice % len(IMAGENS_DEMO)]
        caminho = pasta_imagens / nome_arquivo

        if not caminho.is_file():
            raise CommandError(
                f"Imagem não encontrada: {caminho}. "
                "Coloque os 12 arquivos na pasta seed_images do comando."
            )

        conteudo = caminho.read_bytes()
        anexo = AnexoSolicitacao(
            solicitacao=solicitacao,
            enviado_por=cidadao,
            nome_original=nome_arquivo,
            tipo_conteudo="image/jpeg",
            tamanho_bytes=len(conteudo),
        )
        # ImageField.save grava o arquivo no storage configurado pelo Django
        # (MEDIA_ROOT local ou storage remoto, conforme as settings).
        anexo.arquivo.save(nome_arquivo, ContentFile(conteudo), save=False)
        anexo.save()
        return 1

    @staticmethod
    def _get_or_create_user(User, data, tipo):
        user, created = User.objects.get_or_create(
            email=data["email"],
            defaults={
                "username": data["username"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "cpf": data["cpf"],
                "tipo": tipo,
                "is_active": True,
            },
        )
        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])
        return user

    @staticmethod
    def _registrar_evento(solicitacao, ator, acao, momento, **campos):
        evento = HistoricoSolicitacao.objects.create(
            solicitacao=solicitacao,
            ator=ator,
            acao=acao,
            **campos,
        )
        HistoricoSolicitacao.objects.filter(pk=evento.pk).update(criado_em=momento)
        return evento

    def _criar_historico(self, solicitacao, cidadao, servidor, unidade, status_final, criada_em):
        total = 0
        status_recebida = SolicitacaoZeladoria.Status.RECEBIDA
        self._registrar_evento(
            solicitacao,
            cidadao,
            HistoricoSolicitacao.Acao.CRIACAO,
            criada_em,
            status_novo=status_recebida,
            comentario="Solicitação registrada pelo cidadão.",
        )
        total += 1

        proximo_evento = criada_em + timedelta(hours=3)
        if unidade:
            self._registrar_evento(
                solicitacao,
                servidor,
                HistoricoSolicitacao.Acao.ENCAMINHAMENTO,
                proximo_evento,
                unidade_origem=None,
                unidade_destino=unidade,
                comentario=f"Solicitação encaminhada para {unidade.nome}.",
            )
            total += 1
            proximo_evento += timedelta(hours=3)

        if status_final != "RECEBIDA":
            self._registrar_evento(
                solicitacao,
                servidor,
                HistoricoSolicitacao.Acao.ATRIBUICAO,
                proximo_evento,
                responsavel_novo=servidor,
                comentario="Solicitação atribuída a um servidor responsável.",
            )
            total += 1
            proximo_evento += timedelta(hours=3)

        status_anterior = status_recebida
        for proximo_status in TRANSICOES[status_final]:
            if proximo_status == "CONCLUIDA":
                acao = HistoricoSolicitacao.Acao.CONCLUSAO
            elif proximo_status == "CANCELADA":
                acao = HistoricoSolicitacao.Acao.CANCELAMENTO
            else:
                acao = HistoricoSolicitacao.Acao.ALTERACAO_STATUS

            self._registrar_evento(
                solicitacao,
                servidor,
                acao,
                proximo_evento,
                status_anterior=status_anterior,
                status_novo=proximo_status,
                comentario=COMENTARIOS_STATUS[proximo_status],
            )
            total += 1
            status_anterior = proximo_status
            proximo_evento += timedelta(hours=3)

        SolicitacaoZeladoria.objects.filter(pk=solicitacao.pk).update(
            atualizado_em=proximo_evento - timedelta(hours=3)
        )
        return total
