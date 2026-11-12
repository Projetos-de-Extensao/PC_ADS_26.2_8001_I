from django.core.management.base import BaseCommand
from django.db import transaction

from catalogo.models import ModuloPortal, Tema, Assunto, ServicoCatalogo
from zeladoria.models import UnidadeAtendimento, UnidadeServico


CATALOGO = [
    {
        "tema": "Vias públicas",
        "descricao": "Conservação, manutenção e segurança das vias públicas.",
        "assuntos": [
            {
                "nome": "Conservação de vias",
                "servicos": [
                    {
                        "nome": "Reparo de buracos",
                        "descricao": "Solicitação de reparo de buracos em ruas e avenidas.",
                        "prazo": 10,
                        "ordem": 1,
                    },
                    {
                        "nome": "Pavimentação danificada",
                        "descricao": "Comunicação de trechos com pavimento danificado, solto ou deteriorado.",
                        "prazo": 15,
                        "ordem": 2,
                    },
                    {
                        "nome": "Afundamento de pista",
                        "descricao": "Comunicação de afundamento ou deformação no leito da via.",
                        "prazo": 7,
                        "ordem": 3,
                    },
                ],
            },
            {
                "nome": "Calçadas e acessibilidade",
                "servicos": [
                    {
                        "nome": "Calçada danificada",
                        "descricao": "Solicitação de vistoria e reparo de calçada pública danificada.",
                        "prazo": 20,
                        "ordem": 1,
                    },
                    {
                        "nome": "Obstrução de calçada",
                        "descricao": "Comunicação de obstáculos que impedem a circulação de pedestres.",
                        "prazo": 10,
                        "ordem": 2,
                    },
                    {
                        "nome": "Rampa de acessibilidade danificada",
                        "descricao": "Solicitação de reparo de rampa de acessibilidade em passeio público.",
                        "prazo": 15,
                        "ordem": 3,
                    },
                ],
            },
            {
                "nome": "Sinalização viária",
                "servicos": [
                    {
                        "nome": "Placa de trânsito danificada ou ausente",
                        "descricao": "Comunicação de placa de trânsito danificada, ilegível ou ausente.",
                        "prazo": 12,
                        "ordem": 1,
                    },
                    {
                        "nome": "Pintura de faixa apagada",
                        "descricao": "Solicitação de recomposição de faixas de pedestres e sinalização horizontal.",
                        "prazo": 20,
                        "ordem": 2,
                    },
                ],
            },
        ],
    },
    {
        "tema": "Iluminação pública",
        "descricao": "Manutenção e conservação dos pontos de iluminação pública.",
        "assuntos": [
            {
                "nome": "Manutenção de pontos de luz",
                "servicos": [
                    {
                        "nome": "Lâmpada apagada",
                        "descricao": "Comunicação de luminária pública apagada.",
                        "prazo": 5,
                        "ordem": 1,
                    },
                    {
                        "nome": "Lâmpada piscando",
                        "descricao": "Comunicação de luminária com funcionamento intermitente.",
                        "prazo": 7,
                        "ordem": 2,
                    },
                    {
                        "nome": "Poste danificado",
                        "descricao": "Solicitação de vistoria de poste de iluminação danificado ou inclinado.",
                        "prazo": 3,
                        "ordem": 3,
                    },
                ],
            },
        ],
    },
    {
        "tema": "Limpeza urbana",
        "descricao": "Serviços de limpeza, coleta e remoção de resíduos em espaços públicos.",
        "assuntos": [
            {
                "nome": "Coleta e remoção de resíduos",
                "servicos": [
                    {
                        "nome": "Entulho em via pública",
                        "descricao": "Solicitação de remoção de entulho descartado em logradouro público.",
                        "prazo": 8,
                        "ordem": 1,
                    },
                    {
                        "nome": "Descarte irregular de resíduos",
                        "descricao": "Comunicação de descarte irregular de lixo ou resíduos em área pública.",
                        "prazo": 10,
                        "ordem": 2,
                    },
                    {
                        "nome": "Lixo acumulado em via pública",
                        "descricao": "Solicitação de recolhimento de lixo acumulado em local público.",
                        "prazo": 3,
                        "ordem": 3,
                    },
                ],
            },
            {
                "nome": "Limpeza de logradouros",
                "servicos": [
                    {
                        "nome": "Solicitação de varrição",
                        "descricao": "Solicitação de varrição em rua, praça ou outro logradouro público.",
                        "prazo": 5,
                        "ordem": 1,
                    },
                    {
                        "nome": "Limpeza após feira ou evento",
                        "descricao": "Solicitação de limpeza de espaço público após feira ou evento.",
                        "prazo": 3,
                        "ordem": 2,
                    },
                ],
            },
        ],
    },
    {
        "tema": "Áreas verdes",
        "descricao": "Conservação de árvores, praças, jardins e equipamentos de áreas verdes.",
        "assuntos": [
            {
                "nome": "Arborização urbana",
                "servicos": [
                    {
                        "nome": "Poda de árvore",
                        "descricao": "Solicitação de avaliação e poda de árvore em área pública.",
                        "prazo": 20,
                        "ordem": 1,
                    },
                    {
                        "nome": "Árvore caída",
                        "descricao": "Comunicação de árvore caída em via ou espaço público.",
                        "prazo": 1,
                        "ordem": 2,
                    },
                    {
                        "nome": "Risco de queda de árvore",
                        "descricao": "Solicitação de vistoria de árvore com risco aparente de queda.",
                        "prazo": 2,
                        "ordem": 3,
                    },
                ],
            },
            {
                "nome": "Conservação de praças",
                "servicos": [
                    {
                        "nome": "Manutenção de praça",
                        "descricao": "Comunicação de problemas de conservação em praça ou jardim público.",
                        "prazo": 15,
                        "ordem": 1,
                    },
                    {
                        "nome": "Equipamento de playground danificado",
                        "descricao": "Solicitação de vistoria e manutenção de brinquedo ou equipamento de praça.",
                        "prazo": 10,
                        "ordem": 2,
                    },
                ],
            },
        ],
    },
    {
        "tema": "Drenagem urbana",
        "descricao": "Manutenção da drenagem pluvial e prevenção de alagamentos.",
        "assuntos": [
            {
                "nome": "Drenagem pluvial",
                "servicos": [
                    {
                        "nome": "Bueiro entupido",
                        "descricao": "Solicitação de desobstrução de bueiro ou boca de lobo.",
                        "prazo": 3,
                        "ordem": 1,
                    },
                    {
                        "nome": "Tampa de bueiro danificada",
                        "descricao": "Comunicação de tampa de bueiro quebrada, solta ou ausente.",
                        "prazo": 2,
                        "ordem": 2,
                    },
                    {
                        "nome": "Ponto de alagamento recorrente",
                        "descricao": "Comunicação de local com ocorrência frequente de alagamentos.",
                        "prazo": 10,
                        "ordem": 3,
                    },
                ],
            },
        ],
    },
]

UNIDADES = {
    "Conservação de Vias": {
        "descricao": "Unidade responsável pela conservação de ruas, calçadas e sinalização viária.",
        "temas": ["Vias públicas"],
    },
    "Iluminação Pública": {
        "descricao": "Unidade responsável pela manutenção dos pontos de iluminação pública.",
        "temas": ["Iluminação pública"],
    },
    "Limpeza Urbana": {
        "descricao": "Unidade responsável pela limpeza e remoção de resíduos em logradouros.",
        "temas": ["Limpeza urbana"],
    },
    "Áreas Verdes e Arborização": {
        "descricao": "Unidade responsável pela conservação de árvores, praças e jardins públicos.",
        "temas": ["Áreas verdes"],
    },
    "Drenagem Urbana": {
        "descricao": "Unidade responsável pela manutenção da drenagem pluvial.",
        "temas": ["Drenagem urbana"],
    },
}


class Command(BaseCommand):
    help = "Cria um catálogo de demonstração de zeladoria urbana sem duplicar registros."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        modulo, modulo_criado = ModuloPortal.objects.get_or_create(
            nome="Zeladoria Urbana",
            defaults={
                "descricao": "Serviços municipais de conservação e manutenção da cidade.",
                "ativo": True,
                "ordem": 1,
            },
        )

        contagem = {
            "modulos": int(modulo_criado),
            "temas": 0,
            "assuntos": 0,
            "servicos": 0,
            "unidades": 0,
            "vinculos": 0,
        }
        servicos_por_tema = {}

        for tema_ordem, tema_data in enumerate(CATALOGO, start=1):
            tema, criado = Tema.objects.get_or_create(
                modulo=modulo,
                nome=tema_data["tema"],
                defaults={
                    "descricao": tema_data.get("descricao", ""),
                    "ativo": True,
                    "ordem": tema_ordem,
                },
            )
            contagem["temas"] += int(criado)
            servicos_por_tema[tema.nome] = []

            for assunto_ordem, assunto_data in enumerate(tema_data["assuntos"], start=1):
                assunto, criado = Assunto.objects.get_or_create(
                    tema=tema,
                    nome=assunto_data["nome"],
                    defaults={"ativo": True, "ordem": assunto_ordem},
                )
                contagem["assuntos"] += int(criado)

                for servico_data in assunto_data["servicos"]:
                    servico, criado = ServicoCatalogo.objects.get_or_create(
                        assunto=assunto,
                        nome=servico_data["nome"],
                        defaults={
                            "descricao": servico_data["descricao"],
                            "instrucoes": (
                                "Informe o endereço completo, descreva a ocorrência "
                                "e, se possível, anexe uma fotografia."
                            ),
                            "prazo_estimado_dias": servico_data["prazo"],
                            "formulario_config": {
                                "campos": [
                                    {"nome": "detalhes_local", "tipo": "texto", "obrigatorio": True},
                                    {"nome": "ponto_referencia", "tipo": "texto", "obrigatorio": False},
                                ]
                            },
                            "versao_formulario": 1,
                            "ativo": True,
                            "ordem": servico_data["ordem"],
                        },
                    )
                    contagem["servicos"] += int(criado)
                    servicos_por_tema[tema.nome].append((servico, servico_data["prazo"]))

        for nome_unidade, unidade_data in UNIDADES.items():
            unidade, criado = UnidadeAtendimento.objects.get_or_create(
                nome=nome_unidade,
                defaults={"descricao": unidade_data["descricao"], "ativo": True},
            )
            contagem["unidades"] += int(criado)

            for nome_tema in unidade_data["temas"]:
                for servico, prazo in servicos_por_tema[nome_tema]:
                    _, vinculo_criado = UnidadeServico.objects.get_or_create(
                        unidade=unidade,
                        servico=servico,
                        defaults={"prazo_atendimento_dias": prazo, "ativo": True},
                    )
                    contagem["vinculos"] += int(vinculo_criado)

        self.stdout.write(self.style.SUCCESS("Catálogo de demonstração conferido/inserido."))
        self.stdout.write(f"Módulos novos: {contagem['modulos']}")
        self.stdout.write(f"Temas novos: {contagem['temas']}")
        self.stdout.write(f"Assuntos novos: {contagem['assuntos']}")
        self.stdout.write(f"Serviços novos: {contagem['servicos']}")
        self.stdout.write(f"Unidades novas: {contagem['unidades']}")
        self.stdout.write(f"Vínculos unidade-serviço novos: {contagem['vinculos']}")
        self.stdout.write(
            "Totais atuais — "
            f"módulos: {ModuloPortal.objects.count()}, "
            f"temas: {Tema.objects.count()}, "
            f"assuntos: {Assunto.objects.count()}, "
            f"serviços: {ServicoCatalogo.objects.count()}, "
            f"unidades: {UnidadeAtendimento.objects.count()}, "
            f"vínculos: {UnidadeServico.objects.count()}."
        )
