# Dimensionamento de Computação (EC2)

## Controle do documento

| Campo | Informação |
|---|---|
| Projeto | Portal Cidadão Seguro |
| Versão | 2.0 — revisão documental AP2 |
| Data | 11/11/2026 |
| Aprovação | Pendente de validação pelo grupo |

> **Situação:** este documento distingue arquitetura verificada no repositório de requisitos ainda não implementados ou não comprovados. Não constitui evidência de deploy em produção.

## Objetivo
Dimensionar uma instância EC2 para dois containers na mesma máquina: `web` (Django/DRF/Gunicorn) e `db` (PostgreSQL).

## Classes de análise
| Classe | Papel | Consumo a observar |
|---|---|---|
| Cliente HTTP | Requisita API | Concorrência e latência |
| Serviço web | Processa requisições | CPU, RAM, workers |
| Banco PostgreSQL | Armazena e consulta dados | RAM, cache, I/O |
| Volume EBS/Docker | Mantém dados | Espaço e IOPS |

## Hipótese inicial — não é medição
Para protótipo acadêmico com baixa concorrência, avaliar uma instância de **2 vCPU e 2–4 GiB de RAM**. A escolha final exige medir consumo conjunto do web, banco e sistema operacional. Instâncias com 1 GiB podem ficar pressionadas ao executar ambos os serviços. Não há tipo de instância real confirmado no repositório.

## Método de validação
1. Registrar tipo, região, arquitetura e armazenamento da EC2 real.
2. Medir `docker stats`, memória livre e uso de CPU durante operações representativas.
3. Verificar picos, ajustar tamanho e registrar resultado.
4. Calcular custo mensal a partir da região, horas e preços oficiais vigentes; não assumir valor sem cotação.

## Diagrama PlantUML
```puml
@startuml
class ClienteHTTP
class ServicoWeb { +GET /api/ }
class PostgreSQL { +persistir() }
class VolumePersistente
ClienteHTTP --> ServicoWeb
ServicoWeb --> PostgreSQL
PostgreSQL --> VolumePersistente
@enduml
```

## Evidências pendentes
Tipo EC2 escolhido, métricas, custo mensal calculado e captura de `docker stats`.
