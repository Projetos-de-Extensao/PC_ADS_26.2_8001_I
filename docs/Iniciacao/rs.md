# Requisitos Suplementares

## Controle do documento

| Campo | Informação |
|---|---|
| Projeto | Portal Cidadão Seguro |
| Versão | 2.0 — revisão documental AP2 |
| Data | 11/11/2026 |
| Aprovação | Pendente de validação pelo grupo |

> **Situação:** este documento distingue arquitetura verificada no repositório de requisitos ainda não implementados ou não comprovados. Não constitui evidência de deploy em produção.

## Requisitos não funcionais
| Código | Categoria | Requisito / decisão | Evidência ou lacuna |
|---|---|---|---|
| RS-01 | Desempenho | Medir tempo de resposta da API sob carga representativa; definir meta após teste | Sem medição no ZIP |
| RS-02 | Disponibilidade | Definir janela de serviço e procedimento de recuperação | SLA ainda não acordado |
| RS-03 | Segurança | `SECRET_KEY`, `POSTGRES_PASSWORD`, `DEBUG`, `ALLOWED_HOSTS` via ambiente; banco sem porta pública | Configuração presente; Security Group não comprovado |
| RS-04 | Operação | Implantar Django e PostgreSQL com Docker Compose na EC2 | Compose presente; EC2 não comprovada |
| RS-05 | Persistência | Volume nomeado `postgres_data`; validar após `down`/`up` sem `-v` | Configuração presente; teste prático pendente |
| RS-06 | Dados | Relacional + JSONB, GIN, CRUD e transação atômica | Implementação não encontrada |
| RS-07 | Backup | Criar rotina de `pg_dump`, guardar cópia externa e testar restauração | Pendente |
| RS-08 | Custo | Estimar EC2, EBS, tráfego, snapshots e eventual IP público conforme região | Preços e instância reais pendentes |

## SLA, RPO e RTO
Nenhum SLA contratado, RPO ou RTO medido foi comprovado. Proposta a validar: monitorar disponibilidade e definir metas somente após testes de restauração e aprovação do grupo.

## Riscos e respostas
| Risco | Mitigação |
|---|---|
| Perda de dados no host | Backups externos e teste de restauração |
| Segredos publicados | `.gitignore`, revisão de commits e rotação de credenciais |
| Instância indisponível | Plano de reinício, diagnóstico e rollback |
| Documentação divergente | Vincular cada afirmação a código ou evidência |

## Decisão arquitetural
A solução alvo da AP2 é **EC2 + Docker Compose + PostgreSQL em container**, não ECS/RDS. A instância única não oferece automaticamente alta disponibilidade ou SLA garantido.
